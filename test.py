import tarantool
from connection import Connection

# Подключение к серверу
conn = Connection()

# Вставка данных - передаем кортеж в порядке полей формата
'''
result = conn.eval(f"""
    box.space.users:insert({{
        nil,  
        'session_12345',                         
        '250011223344550',
        '+79123456789',                           
        'user@domain.com',
        {{'192.168.1.100', '10.0.0.1'}},            
        {{'2001:db8::/64', '2001:db8:1::/64'}},     
        '00-11-22-33-44-55' 
    }})
    """
)
'''
'''
result = conn.insert('users', (None,
        'session_12345',
        '250011223344550',
        '+79123456789',
        'user@domain.com',
        ('192.168.1.100', '10.0.0.1'),
        ('2001:db8::/64', '2001:db8:1::/64'),
        '00-11-22-33-44-55'))

print("Вставленная запись:", result)

'''

space = conn.space("users")
#result = space.select(index = "primary")
#result = conn.call('select_rows', ('users', ['Id','Session_Id','IMSI'], {'limit': 10}))
result = conn.call('select_with_values', ('users','session+ip_index','gx-test.epc.mnc099.mcc999.3gppnetwork.org;60461;10684;1',"1"))
#result = conn.call('select_with_value', ('users','framed_ip_address_index',"225"))

print(len(result[0]))