import tarantool

def Connection():
    try:
        conn = tarantool.Connection('localhost', 3301)
        return conn
    except Exception as e:
        print(f"ошибка подключения {e}")
        return False