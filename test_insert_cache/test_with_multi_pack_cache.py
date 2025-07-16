from connection import Connection
import time
from creation_test_data import creation_data

conn = Connection()

data1 = [(str(i), "3") for i in range(100000)]
data2 = [(str(i), "\x00\xFF\xAA\xBB") for i in range(100000)]
batch_size = 1000

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

start = time.time()

for batch in chunks(data1, batch_size):
    for record in batch:
        conn.insert('cache1', record)

end = time.time() - start

print(f"время вставки в cache1:{end}, скорость:{100000/end}")

start = time.time()

for batch in chunks(data2, batch_size):
    for record in batch:
        conn.insert('cache2', record)

end = time.time() - start

print(f"время вставки в cache2:{end}, скорость:{100000/end}")