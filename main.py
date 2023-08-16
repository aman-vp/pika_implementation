from fastapi import FastAPI
import pika

app = FastAPI()


def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_series = [0, 1]
    for i in range(2, n):
        fib_series.append(fib_series[i - 1] + fib_series[i - 2])

    return fib_series


@app.get("/fibo")
async def send_fibonacci_to_queue(n: int):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))  # Change this to your RabbitMQ server address
    channel = connection.channel()
    channel.queue_declare(queue='fibonacci')

    fib_series = fibonacci(n)

    for num in fib_series:
        channel.basic_publish(exchange='', routing_key='fibonacci', body=str(num))
        print(f"Sent: {num}")

    connection.close()

    return {"message": "Fibonacci series sent to queue"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
