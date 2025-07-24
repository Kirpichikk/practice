import socket
from connection import Connection
import time
import msgpack
import json

from decoder import process_message_stream

HOST = '127.0.0.1'  # Локальный адрес
PORT = 65432        # Порт для прослушивания

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Сервер запущен на {HOST}:{PORT}. Ожидание подключения...")
    conn_bd = Connection()

    timee = "dhtvz"
    data = b''
    conn, addr = s.accept()
    with conn:
        print(f"Подключен клиент: {addr}")
        while True:
            buf = conn.recv(7111120)
            data += buf
            if data.endswith(b'END_MSG'):
                data = data[:-7]
                break

        if not data:
            print("Нет данных от клиента.")
        else:
            start = time.time()
            result = process_message_stream(data, conn_bd)
            end = time.time() - start
            end = str(end)
            mail = msgpack.packb(result)
            mail += b'END_MSG'
            conn.sendall(end.encode())
            conn.sendall(mail)
            print("Ответ отправлен.")
    print("Соединение закрыто.")