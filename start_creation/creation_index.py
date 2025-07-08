from connection import Connection

def create_index_primary(conn, name, part, space_name, parameter_unique):
    try:
        result = conn.eval(f"""
        index = box.space.{space_name}:create_index('{name}', {{
                parts={{'{part}'}},
                unique = {parameter_unique},
                sequence = 'id_seq'
            }})
            return true
        """)
        return result.data[0]

    except Exception as e:
        print(f"ошибка создания индекса {e}")
        return False

def create_index(conn, name, part, space_name, parameter_unique):
    try:
        result = conn.eval(f"""
        index = box.space.{space_name}:create_index('{name}', {{
                parts={{'{part}'}},
                unique = {parameter_unique}
            }})
            return true
        """)
        return result.data[0]

    except Exception as e:
        print(f"ошибка создания индекса {e}")
        return False

def create_index_array(conn, name, part, space_name, parameter_unique):
    try:
        result = conn.eval(f"""
        index = box.space.{space_name}:create_index('{name}', {{
                type = 'tree',
                parts={{
                    {{
                        field = '{part}[*]',
                        type = 'string',
                        is_nullable = true 
                    }}
                }},   
                unique = {parameter_unique}
            }})
            return true
        """)
        return result.data[0]

    except Exception as e:
        print(f"ошибка создания индекса {e}")
        return False

conn = Connection()

format_info = conn.eval("return box.space.users:format()")
names = [i['name'] for i in format_info[0][1:]]

create_index_primary(conn, "primary","Id", "users", "true")

for name in names:
    if name in ["framed_ip_address", "framed_ipv6_prefix"]:
        create_index_array(conn, name + "_index", name, "users", "false")
    else:
        create_index(conn, name+"_index",name, "users", "false")
