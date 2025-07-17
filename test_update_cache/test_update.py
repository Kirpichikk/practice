import time

from update_data_cache import update_value
from connection import Connection

conn = Connection()

amount = [5,50,500,5000,50000,500000]

print("cache1")
for i in amount:
    start = time.time()
    flag = 0
    for j in range(i):
        if flag % 2 == 0:
            update_value(conn,'cache1','3','0')
        else:
            update_value(conn, 'cache1', '3', '1')
        flag += 1
    end = time.time() - start
    print(f'время работы {i}: {end}')

print("cache2")
for i in amount:
    start = time.time()
    flag = 0
    for j in range(i):
        if flag % 2 == 0:
            update_value(conn,'cache2','3',b'\x00')
        else:
            update_value(conn, 'cache2', '3', b'\x01')
    end = time.time() - start
    print(f'время работы {i}: {end}')