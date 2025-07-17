import time
from connection import Connection
from creation_data.creation_test_data_cache import creation_data

conn = Connection()
data1 = creation_data(1)
data2 = creation_data(2)

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