#нужно написать функцию, которые выводят определённое колиечство полей

from connection import Connection
import time

conn = Connection()

columns = ['Id','Session_Id','IMSI','MSDN','NAI','framed_ip_address','framed_ipv6_prefix','called_station_id']
for i in range(len(columns)):
    start = time.time()
    result = conn.call('select_rows', ('users', columns[:i+1]))
    end = time.time() - start
    print(f'время выгрузки {i} строк: {end}')




