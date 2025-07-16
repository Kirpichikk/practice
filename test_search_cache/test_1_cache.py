from connection import Connection
import time

conn = Connection()

print("выгрузка cache1")
start = time.time()
conn.call('select_rows', ('cache1', ['key']))
end = time.time() - start
print(f'время выгрузки key: {end}')

start = time.time()
conn.call('select_rows', ('cache1', ['value']))
end = time.time() - start
print(f'время выгрузки value: {end}')

start = time.time()
conn.call('select_rows', ('cache1', ['key','value']))
end = time.time() - start
print(f'время выгрузки всего: {end}')

print("выгрузка cache2")
start = time.time()
conn.call('select_rows', ('cache2', ['key']))
end = time.time() - start
print(f'время выгрузки key: {end}')

start = time.time()
conn.call('select_rows', ('cache2', ['value']))
end = time.time() - start
print(f'время выгрузки value: {end}')

start = time.time()
conn.call('select_rows', ('cache2', ['key','value']))
end = time.time() - start
print(f'время выгрузки всего: {end}')