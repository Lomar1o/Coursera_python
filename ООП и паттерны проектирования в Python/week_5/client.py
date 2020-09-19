import socket
from time import time


class Client:
    """
    Клиент для взаимодействия с сервером.
    """
    def __init__(self, host, port, timeout=None):
        # Устанавливаем соединение с серевром по заданным хост, порт, таймаут
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def _send(self, data):
        # Отправляем запрос и получаем ответ от сервера
        try:
            self.sock.send(data.encode('utf8'))
            return self.sock.recv(1024).decode('utf8')
        except socket.error as err:
            raise ClientError(err)

    def _status(self, data):
        # Проверяем статус сервера
        if data[0:2] != 'ok':
            raise ClientError
        return data

    def put(self, metric, value, timestamp=None):
        # Отправляем команду на сервер
        timestamp = timestamp or int(time())
        self._status(self._send(f'put {metric} {value} {timestamp}\n'))

    def get(self, metric):
        '''
        Получаем ответ от сервера
        '''
        data = {}
        response = self._status(self._send(f'get {metric}\n'))
        response = response.strip('\n').split('\n')
        try:
            for line in response[1:]:
                metric, value, timestamp = line.split()
                if metric not in data:
                    data[metric] = list()
                data[metric].append((int(timestamp), float(value)))
                data[metric].sort(key=lambda x: x[0])
        except (IndexError, ValueError) as err:
            raise ClientError(err)
        return data


class ClientError(Exception):

    def __init__(self, massage='Don`t work:'):
        self.massage = massage


if __name__ == '__main__':
    client = Client('127.0.0.1', 8180)
    print(client.put('palm.cpu', 3.0))
    print(client.put('palm.cpu', 4.0))
    print(client.put('palm', 3.0))
    print(client.put('cpu', 3.0))
    print(client.get('*'))


