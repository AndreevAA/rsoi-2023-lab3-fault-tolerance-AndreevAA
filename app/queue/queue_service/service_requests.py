import requests
from queue_service.circuit_breaker import CircuitBreaker

circuit_breaker = CircuitBreaker()

# Получения данных из очереди
def get_data_from_service(service_url, headers={}, timeout=10):
    if circuit_breaker.try_connect(service_url):
        try:
            response = requests.get(service_url, timeout=timeout, headers=headers)
            circuit_breaker.connection_successful(service_url)
            return response
        except:
            circuit_breaker.connection_error(service_url)
            return None
