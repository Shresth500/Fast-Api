import time
from collections import defaultdict, deque
from fastapi import HTTPException, Depends
from validate_api_key import verify_token


# ---------------------------------------------------------------------------
# 3. Rate Limiter — sliding window, per API key (in-memory; use Redis for
#    multi-instance deployments)
# ---------------------------------------------------------------------------
RATE_LIMIT = 20          # requests
RATE_WINDOW = 60         # seconds
request_log: dict[str, deque] = defaultdict(deque)


def check_rate_limit(user: dict = Depends(verify_token)) -> dict:
    now = time.time()
    window = request_log[user["id"]]

    while window and window[0] < now - RATE_WINDOW:
        window.popleft()

    if len(window) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    window.append(now)
    return user