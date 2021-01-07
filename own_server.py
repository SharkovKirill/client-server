import asyncio
import time


host = '127.0.0.1'
port = 8888
#host = input('Enter host: ')
#port = int(input('Enter port: '))


class ClientServerProtocol(asyncio.Protocol):
    list_key = []
    list_value = []
    list_timestamp = []

    def connection_made(self, transport):
        #peername = transport.get_extra_info('peername')
        #print('Connection from {}'.format(peername))
        self.transport = transport

    def _message_processing(self, message, list_key, list_value, list_timestamp):
        try:
            command = message[:3]
        except:
            return 'error\nwrong command\n\n'

        if command == 'put':
            try:
                key, value, timestamp = message.split()[1:]
                check = 0
                for test in range(len(list_key)):
                    if list_key[test] == key and list_timestamp[test] == timestamp:
                        list_value[test] = value
                        check = 1
                if check == 0:
                    list_key.append(key)
                    list_value.append(value)
                    list_timestamp.append(timestamp)
                return 'ok\n\n'
            except:
                return 'error\nwrong command\n\n'

        elif command == 'get':
            key = message.split()[1]

            if len(message.split()) != 2:
                return 'error\nwrong command\n\n'

            if key == '*':
                if len(list_key) != 0:
                    answer = 'ok'
                    for k in range(len(list_key)):
                        answer +='\n'+list_key[k]+' '+list_value[k]+' '+list_timestamp[k]
                    answer+='\n\n'
                    return answer
                else:
                    return 'ok\n\n'

            elif key not in list_key:
                return 'ok\n\n'

            else:
                answer = 'ok'
                for k in range(len(list_key)):
                    if key == list_key[k]:
                        answer += '\n' + list_key[k] + ' ' + list_value[k] + ' ' + list_timestamp[k]
                answer += '\n\n'
                return answer

        else:
            return 'error\nwrong command\n\n'





    def data_received(self, data):
        try:
            message = data.decode()
        except:
            return 'error\nwrong command\n\n'
        message_to_send = self._message_processing(message, ClientServerProtocol.list_key, ClientServerProtocol.list_value, ClientServerProtocol.list_timestamp)
        self.transport.write(message_to_send.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

run_server(host, port)
