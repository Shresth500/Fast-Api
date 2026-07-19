"""
Simple API Gateway implemented in Python using FastAPI.

Features:
- Dynamic routing to multiple backend microservices
- API key authentication
- Per-client rate limiting (in-memory, sliding window)
- Request/response logging
- Centralized error handling
- Async forwarding via httpx (non-blocking)

Run with:
    pip install fastapi uvicorn httpx --break-system-packages
    uvicorn api_gateway:app --reload --port 8080
"""

import json
import time
import logging

import httpx
from fastapi import FastAPI, Request, HTTPException, Depends
from rate_limitter import check_rate_limit
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_gateway")

app = FastAPI(title="Python API Gateway")

# ---------------------------------------------------------------------------
# 1. Service Registry — maps a public path prefix to an internal backend URL
# ---------------------------------------------------------------------------
SERVICE_ROUTES = {
    # "auth": "http://localhost:8000",      # auth-service
    "chat": "http://localhost:8001/chat-window",     # chat-service
}



# ---------------------------------------------------------------------------
# 4. Gateway Route — catches all requests and forwards to the right service
# ---------------------------------------------------------------------------
@app.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway(
    service: str,
    path: str,
    request: Request,
    user: dict = Depends(check_rate_limit),
):
    print(f"service: {service}")
    print(f"path: {path}")
    print(f"Request headers: {request.headers}")
    print(f"Request query params: {request.query_params}")
    print(f"Request method: {request.method}")
    if service not in SERVICE_ROUTES:
        raise HTTPException(status_code=404, detail=f"Unknown service '{service}'")
 
    target_url = f"{SERVICE_ROUTES[service]}/{path}"
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("authorization", None)  # don't leak the raw token downstream
    headers["x-authenticated-user"] = json.dumps(user)  # trusted header for backends
    headers["x-gateway-secret"] = "internal-only-shared-secret"  # backend can check this came via gateway
 
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=body,
            )
    except httpx.ConnectError:
        logger.error(f"Backend unreachable: {target_url}")
        raise HTTPException(status_code=502, detail="Bad Gateway: backend unreachable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Gateway Timeout")
 
    duration_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        f"{request.method} /{service}/{path} -> {response.status_code} "
        f"({duration_ms}ms) [user={user}]"
    )
 
    return JSONResponse(
        status_code=response.status_code,
        content=response.json() if response.content else {},
    )