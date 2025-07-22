import time
from connection import Connection
from creation_data.creation_test_data_cache import creation_data

conn = Connection()

data1 = creation_data(1)
data2 = creation_data(2)
batch_size = 2500

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

start = time.time()

for batch in chunks(data1, batch_size):
    result = conn.call('insert_batch_cache1', (batch,))

conn.call('wait_completion')

end = time.time() - start

print(f"время вставки в cache1:{end}, скорость:{100000/end}")

start = time.time()

for batch in chunks(data2, batch_size):
    result = conn.call('insert_batch_cache2', (batch,))

conn.call('wait_completion')

end = time.time() - start

print(f"время вставки в cache2:{end}, скорость:{100000/end}")
