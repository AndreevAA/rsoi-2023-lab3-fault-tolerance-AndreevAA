import time
import random

CIRCUIT_BREAKER_BAN_TIME = 60 * 60  # Время блокировки после превышения количества попыток подключения
CIRCUIT_BREAKER_CONNECT_CHANCE = 25  # Вероятность успешного подключения при блокировке
CIRCUIT_BREAKER_CONNECT_TRIES = 5  # Количество попыток подключения до блокировки

class CircuitBreaker:
    instance = None

    @classmethod
    def new(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def init(self):
        self.urls_data = {}  # Словарь для хранения данных о подключениях к URL

    def try_connect(self, url):
        ans = True

        if self.urls_data[url][0] == -1:
            if self.urls_data[url][1] < time.time():
                ans = False
            elif random.randint(0, 100) >= CIRCUIT_BREAKER_CONNECT_CHANCE:
                ans = False
        
        return ans

    def connection_error(self, url):
        if self.urls_data[url][0] == -1:
            self.urls_data[url][1] = time.time() + CIRCUIT_BREAKER_BAN_TIME
            return

        self.urls_data[url][0] += 1
        if self.urls_data[url][0] >= CIRCUIT_BREAKER_CONNECT_TRIES:
            self.urls_data[url][0] = -1
            self.urls_data[url][1] = time.time() + CIRCUIT_BREAKER_BAN_TIME

    def connection_successful(self, url):
        self.urls_data[url][0] = 0

