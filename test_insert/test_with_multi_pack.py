from connection import Connection
import time
from creation_test_data import creation_data

conn = Connection()

data = creation_data(True)
batch_size = 1000

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
start = time.time()

for batch in chunks(data, batch_size):
    for record in batch:
        conn.insert('users', record)

end = time.time() - start

print(f"время вставки:{end}, скорость:{100000/end}")