import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class DictForSaveMetric:
    """Класс для работы с хранилищем данных"""
    def __init__(self):
        self.dct = {}

    def put(self, data):
        metric, value, timestamp = data
        if metric not in self.dct:
            self.dct[metric] = {}
        try:
            self.dct[metric][int(timestamp)] = float(value)
        except ValueError:
            return 'error\nwrong command\n\n'
        return 'ok\n\n'

    def get(self, metric):
        metric = ''.join(metric).strip()
        result = f'ok\n'
        if metric == '*':
            for key, values in self.dct.items():
                for timestamp, value in values.items():
                    result += f'{key} {value} {timestamp}\n'
        if metric in self.dct:
            for timestamp, value in self.dct[metric].items():
                result += f'{metric} {value} {timestamp}\n'
        elif metric not in self.dct:
            return f'{result}\n'
        else:
            return 'error\nwrong command\n\n'
        return f'{result}\n'


class ClientServerProtocol(asyncio.Protocol):

    dct = DictForSaveMetric()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        try:
            command, *data = data.split(' ')
        except (AttributeError, ValueError) as err:
            raise ClientError(err)
        if command == 'put' and len(data) == 3:
            return self.dct.put(data)
        elif command == 'get' and len(data) == 1:
            return self.dct.get(data)
        else:
            return 'error\nwrong command\n\n'


class ClientError(Exception):

    def __init__(self, message='Don`t work:'):
        self.message = message


if __name__ == '__main__':
    start = run_server('127.0.0.1', 8180)
