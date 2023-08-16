from fastapi import FastAPI, BackgroundTasks
import pika
import concurrent.futures
from fibonacci_utils import send_fibonacci_to_queue

app = FastAPI()


def get_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))  # Change this to your RabbitMQ server address
    return connection.channel()


def run_in_thread(func, *args, **kwargs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.submit(func, *args, **kwargs).result()


@app.post("/calculate-fibonacci/")
async def calculate_fibonacci(background_tasks: BackgroundTasks, n: int):
    channel = get_channel()
    background_tasks.add_task(run_in_thread, send_fibonacci_to_queue, channel, n)

    return {"message": f"Fibonacci series calculation enqueued for {n} numbers"}
