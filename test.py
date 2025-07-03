import tarantool
from connection import Connection

# Подключение к серверу
conn = Connection()

# Выбор пространства
space = conn.space('users')

# Вставка данных - передаем кортеж в порядке полей формата
result = space.auto_increment((
    '550e8400-e29b-41d4-a716-446655440000',  # Id (uuid)
    'session_12345',                          # Session_Id
    '250011223344550',                        # IMSI
    '+79123456789',                           # MSDN
    'user@domain.com',                        # NAI
    ['192.168.1.100', '10.0.0.1'],            # framed_ip_address
    ['2001:db8::/64', '2001:db8:1::/64'],     # framed_ipv6_prefix
    '00-11-22-33-44-55'                       # called_station_id
))

print("Вставленная запись:", result.data)
