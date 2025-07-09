import time
from connection import Connection

conn = Connection()

start = time.time()

for i in range(100000):
    conn.insert('users', (None,
                          'session_12345',
                          '250011223344550',
                          '+79123456789',
                          'user@domain.com',
                          ('192.168.1.100', '10.0.0.1'),
                          ('2001:db8::/64', '2001:db8:1::/64'),
                          '00-11-22-33-44-55'))

end = time.time() - start

print(f"время вставки:{end}, скорость:{100000/end}")