from connection import Connection
import time

conn = Connection()

value = ['gx-test.epc.mnc099.mcc999.3gppnetwork.org;60461;10684;1','gx-test.epc.mnc099.mcc999.3gppnetwork.org;60461;10684','gx-test.epc.mnc099.mcc999.3gppnetwork.org;60461','gx-test.epc.mnc099.mcc999.3gppnetwork.org','gx-test.epc.mnc099.mcc999.3gppnetwork','gx-test.epc.mnc099.mcc999','gx-test.epc.mnc099','gx-test.epc']

start = time.time()
result = conn.call('select_with_values', ('users','session+ip_index',value[0],"225"))
end = time.time() - start

print(f'время выгрузки {value[0]} и "225": {end}')

for i in value[1:]:
    start = time.time()
    conn.call('select_with_values', ('users','session+ip_index',i,"225.38", {'iterator':'GE'}))
    end = time.time() - start
    print(f'время выгрузки {i} и "225": {end}')