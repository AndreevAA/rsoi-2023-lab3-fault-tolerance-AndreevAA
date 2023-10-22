import time
import random

CIRCUIT_BREAKER_BAN_TIME = 60 * 60
CIRCUIT_BREAKER_CONNECT_CHANCE = 25
CIRCUIT_BREAKER_CONNECT_TRIES = 5


class CircuitBreaker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CircuitBreaker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.urls_data = {}

    def try_connect(self, url):
        res = True

        if url in self.urls_data.keys():
            if self.urls_data[url][0] == -1:
                if self.urls_data[url][1] < time.time():
                    res = False
                else:
                    if random.randint(0, 100) >= CIRCUIT_BREAKER_CONNECT_CHANCE:
                        res = False
        return res
