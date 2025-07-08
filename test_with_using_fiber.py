import time
from connection import Connection

conn = Connection()

data = [('session_12345','250011223344550','+79123456789','user@domain.com',('192.168.1.100', '10.0.0.1'),('2001:db8::/64', '2001:db8:1::/64'),'00-11-22-33-44-55') for _ in range(100000)]
batch_size = 1000  # размер батча

# Функция для разбиения на батчи
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
start = time.time()

for batch in chunks(data, batch_size):
    result = conn.call('insert_batch', (batch,))

end = time.time() - start

print(f"время вставки:{end}, скорость:{100000/end}")