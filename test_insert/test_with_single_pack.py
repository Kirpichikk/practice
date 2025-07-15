import time
from connection import Connection
from creation_test_data import creation_data

conn = Connection()
data = creation_data(True)
start = time.time()

for i in data:
    conn.insert('users', i)

end = time.time() - start

print(f"время вставки:{end}, скорость:{100000/end}")