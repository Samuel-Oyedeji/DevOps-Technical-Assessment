import os
import requests
from prometheus_client import start_http_server, Gauge
from time import sleep

# Define metrics
messages_metric = Gauge('rabbitmq_individual_queue_messages', 'Total messages', ['host', 'vhost', 'queue'])
messages_ready_metric = Gauge('rabbitmq_individual_queue_messages_ready', 'Ready messages', ['host', 'vhost', 'queue'])
messages_unack_metric = Gauge('rabbitmq_individual_queue_messages_unacknowledged', 'Unacknowledged messages', ['host', 'vhost', 'queue'])

# Environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

def fetch_queue_metrics():
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    try:
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        queues = response.json()

        for queue in queues:
            host = RABBITMQ_HOST
            vhost = queue['vhost']
            name = queue['name']
            messages_metric.labels(host=host, vhost=vhost, queue=name).set(queue['messages'])
            messages_ready_metric.labels(host=host, vhost=vhost, queue=name).set(queue['messages_ready'])
            messages_unack_metric.labels(host=host, vhost=vhost, queue=name).set(queue['messages_unacknowledged'])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus exporter running on port 8000")
    while True:
        fetch_queue_metrics()
        sleep(15)
