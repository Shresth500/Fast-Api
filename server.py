from client.rq_client import queue
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from queues.worker import process_query


load_dotenv()

app = FastAPI()

@app.get('/')
def root():
    return {"status":"Server is up and running"}


@app.post('/chat')
def chat(
        query:str = Query(..., description="The chat query of user")
):
    job = queue.enqueue(process_query, query)
    print(queue)
    return {"status":"queued","job_id":job.id}


@app.get('/job-status')
def get_result(
    job_id:str = Query(...,description="Job Id")
):
    job = queue.fetch_job(job_id=job_id)
    print(queue)
    result = job.return_value()
    return {"result":result}