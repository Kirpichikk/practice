from connection import Connection
space_name = "users"
conn = Connection()

if conn:
    try:
        if conn.eval(f"return box.space.{space_name} ~= nil").data[0]:
            print(f"Пространство {space_name} уже существует")
        else:
            result = conn.eval(f"""
               local space = box.schema.space.create('{space_name}', {{
                   if_not_exists = true,
                   engine = 'vinyl',
                   format = {{
                       {{name = 'Id', type = 'unsigned'}},
                       {{name = 'Session_Id', type = 'string'}},
                       {{name = 'IMSI', type = 'string', is_nullable = true}},
                       {{name = 'MSDN', type = 'string', is_nullable = true}},
                       {{name = 'NAI', type = 'string', is_nullable = true}},
                       {{name = 'framed_ip_address', type = 'array', is_nullable = true}},
                       {{name = 'framed_ipv6_prefix', type = 'array', is_nullable = true}},
                       {{name = 'called_station_id', type = 'string'}}
                   }}
               }})
               return true
           """)

            print(f"Пространство {space_name} создано")

            conn.eval(f"""
                box.schema.sequence.create('id_seq', {{
                     step = 1,
                     if_not_exists = true
                    }}
                )
                return true
            """)

    except Exception as e:
        print(f"Ошибка создания: {e}")
