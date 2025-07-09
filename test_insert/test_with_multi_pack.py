from connection import Connection
import time

conn = Connection()

data = [(None,'session_12345','250011223344550','+79123456789','user@domain.com',('192.168.1.100', '10.0.0.1'),('2001:db8::/64', '2001:db8:1::/64'),'00-11-22-33-44-55') for _ in range(100000)]
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