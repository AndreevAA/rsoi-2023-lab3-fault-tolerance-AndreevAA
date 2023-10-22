import requests
from queue_service.circuit_breaker import CircuitBreaker

circuit_breaker = CircuitBreaker()

# Проверка соединения с сервисом
def is_connection_to_service_success(service_url):
    return circuit_breaker.try_connect(service_url)

# Обработчик данных в сервисе
def data_from_service(service_url, headers={}, timeout=10, data={}, type_req):
    try:
        if type_req=="get":
            response = requests.get(service_url, timeout=timeout, headers=headers)
        elif type_req=="post":
            response = requests.post(service_url, timeout=timeout, headers=headers, json=data)
        elif type_req=="delete":
            response = requests.delete(service_url, timeout=timeout, headers=headers)
        
        circuit_breaker.connection_successful(service_url)
        return response
    except:
        circuit_breaker.connection_error(service_url)
        return None

# Получение данных из сервиса
def get_data_from_service(service_url, headers={}, timeout=10):
    if is_connection_to_service_success(service_url):
        return data_from_service(service_url, headers, timeout, data, "get")

# Пост данных в сервис
def post_data_from_service(service_url, headers={}, timeout=10, data={}):
    if is_connection_to_service_success(service_url):
        return data_from_service(service_url, headers, timeout, data, "post")

# Удаление данных из сервиса
def delete_data_from_service(service_url, headers={}, timeout=10):
    if is_connection_to_service_success(service_url):
        return data_from_service(service_url, headers, timeout, data, "delete")

