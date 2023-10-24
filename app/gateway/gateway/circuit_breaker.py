import time
import random

CIRCUIT_BREAKER_BAN_TIME = 60 * 60
CIRCUIT_BREAKER_CONNECT_CHANCE = 25
CIRCUIT_BREAKER_CONNECT_TRIES = 5


class CircuitBreaker:
    instance = None

    @classmethod
    def new(cls):
        cls.instance = cls.instance or cls()
        return cls.instance

    def __init__(self):
        self.urls_data = {}

    def try_connect(self, url):
        data = self.urls_data.setdefault(url, [0, time.time()])
        if data[0] == -1 and data[1] >= time.time():
            return False
        elif data[0] == -1 or random.randint(0, 100) >= CIRCUIT_BREAKER_CONNECT_CHANCE:
            return False
        return True

    def connection_error(self, url):
        data = self.urls_data[url]
        data[0] += 1
        if data[0] >= CIRCUIT_BREAKER_CONNECT_TRIES:
            data[0] = -1
            data[1] = time.time() + CIRCUIT_BREAKER_BAN_TIME

    def connection_successful(self, url):
        self.urls_data[url][0] = 0
