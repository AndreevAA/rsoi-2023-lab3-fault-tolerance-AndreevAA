import requests
from gateway.circuit_breaker import CircuitBreaker

circuit_breaker = CircuitBreaker()

def make_request(method, service_url, headers={}, timeout=10, data=None):
    if circuit_breaker.try_connect(service_url):
        try:
            response = requests.request(method, service_url, timeout=timeout, headers=headers, json=data)
            circuit_breaker.connection_successful(service_url)
            return response
        except:
            circuit_breaker.connection_error(service_url)
            return None

def get_data_from_service(service_url, headers={}, timeout=10):
    return make_request("GET", service_url, headers=headers, timeout=timeout)


def post_data_from_service(service_url, headers={}, timeout=10, data={}):
    return make_request("POST", service_url, headers=headers, timeout=timeout, data=data)


def delete_data_from_service(service_url, headers={}, timeout=10):
    return make_request("DELETE", service_url, headers=headers, timeout=timeout)
