import time

from delete_data_cache import delete_data
from connection import Connection

conn = Connection()

print("cache1")
start = time.time()
for i in range(100000):
    delete_data(conn,'cache1',f'{i}',)
end = time.time() - start
print(f'время удаление: {end}')

print("cache2")
start = time.time()
for i in range(100000):
    delete_data(conn,'cache2',f'{i}',)
end = time.time() - start
print(f'время удаление: {end}')