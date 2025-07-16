from connection import Connection
import time

conn = Connection()

start = time.time()
conn.call('select_with_value', ('cache1','cache1_key','99999'))
end = time.time() - start
print(f'время выгрузки : {end}')

start = time.time()
conn.call('select_with_value', ('cache2','cache2_key','99999'))
end = time.time() - start
print(f'время выгрузки : {end}')