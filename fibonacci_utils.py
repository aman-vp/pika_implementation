import pika


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


def send_fibonacci_to_queue(channel, n):
    channel.queue_declare(queue='fibonacci')

    try:
        fib_series = fibonacci(n)

        for num in fib_series:
            channel.basic_publish(exchange='', routing_key='fibonacci', body=str(num))
            # print(f"Sent: {num}")
        print("task succcessfull")
    except Exception as e:
        print(f"Error: {e}")
        channel.queue_declare(queue='dead_letter')
        channel.basic_publish(exchange='', routing_key='dead_letter', body=f"Fibonacci error: {e}")
