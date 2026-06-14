from redis import Redis
from rq import Queue, SimpleWorker

Redis(host="localhost", port=6379).flushall()

redis_conn = Redis(
    host="localhost",
    port=6379
)

queue = Queue(connection=redis_conn)

worker = SimpleWorker(
    [queue],
    connection=redis_conn
)

if __name__ == "__main__":
    worker.work()