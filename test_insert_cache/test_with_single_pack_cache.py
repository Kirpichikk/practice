import time
from connection import Connection

conn = Connection()
data1 = [(str(i), "3") for i in range(100000)]
data2 = [(str(i), "\x00\xFF\xAA\xBB") for i in range(100000)]

start = time.time()

for i in data1:
    conn.insert('cache1', i)

end = time.time() - start

print(f"время вставки в cache1:{end}, скорость:{100000/end}")

start = time.time()

for i in data2:
    conn.insert('cache2', i)

end = time.time() - start

print(f"время вставки в cache2:{end}, скорость:{100000/end}")