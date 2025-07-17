import time
from connection import Connection
from creation_data.creation_test_data import creation_data

conn = Connection()

data = creation_data()
batch_size = 2500

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

start = time.time()

for batch in chunks(data, batch_size):
    result = conn.call('insert_batch', (batch,))

conn.call('wait_completion')

end = time.time() - start

print(f"время вставки:{end}, скорость:{100000/end}")