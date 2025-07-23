import socket

import msgpack

from coder import only_insert, only_select, insert_or_select, speed_test_data

HOST = '127.0.0.1'  # Локальный адрес сервера
PORT = 65432        # Порт сервера

data = only_select()
data += b'END_MSG'
print(data)
print(len(data))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    s.sendall(data)
    #time = s.recv(1024)
    result = b''
    while True:
        buf = s.recv(7111120)
        result += buf
        if result.endswith(b'END_MSG'):
            result = result[:-7]
            break

    re = msgpack.unpackb(result)
    print("Получено")
    print(re)
print("Соединение закрыто.")