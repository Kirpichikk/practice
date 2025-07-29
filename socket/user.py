import socket

import msgpack

import coder

HOST = '127.0.0.1'  # Локальный адрес сервера
PORT = 65432        # Порт сервера

name_functions = ["only_insert", "only_select", "insert_or_select", "speed_test_data"]

for name in name_functions:
    func = getattr(coder, name)
    data = func()
    data += b'END_MSG'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        s.sendall(data)
        time = s.recv(1024)
        print(f' скорость выполнения: {time.decode()}')
        result = b''
        while True:
            buf = s.recv(7111120)
            result += buf
            if result.endswith(b'END_MSG'):
                result = result[:-7]
                break

        re = msgpack.unpackb(result)
        print("Получено")
    print("Соединение закрыто.")