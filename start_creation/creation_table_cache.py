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
                   format = {{
                       {{name = 'key', type = 'unsigned'}},
                       {{name = 'value', type = 'string'}},
                   }}
               }})
               return true
           """)

            print(f"Пространство {space_name} создано")

            conn.eval(f"""
                box.schema.sequence.create('key_seq', {{
                     step = 1,
                     if_not_exists = true
                    }}
                )
                return true
            """)

    except Exception as e:
        print(f"Ошибка создания: {e}")
