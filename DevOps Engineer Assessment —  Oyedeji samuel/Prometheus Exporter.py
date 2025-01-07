from prometheus_client import start_http_server, Gauge
import requests

# Define metrics
message_gauge = Gauge('rabbitmq_individual_queue_messages', 'Total messages', ['host', 'vhost', 'queue'])

def fetch_metrics():
    # Fetch and update metrics here
    pass

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        fetch_metrics()
