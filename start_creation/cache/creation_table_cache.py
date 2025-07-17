from connection import Connection
space_name1 = "cache1"
space_name2 = "cache2"
conn = Connection()

if conn:
    try:
        if conn.eval(f"return box.space.{space_name1} ~= nil").data[0]:
            print(f"Пространство {space_name1} уже существует")
        else:
            result = conn.eval(f"""
               local space = box.schema.space.create('{space_name1}', {{
                   if_not_exists = true,
                   format = {{
                       {{name = 'key', type = 'string'}},
                       {{name = 'value', type = 'string'}},
                   }}
               }})
               return true
           """)

            print(f"Пространство {space_name1} создано")

        if conn.eval(f"return box.space.{space_name2} ~= nil").data[0]:
            print(f"Пространство {space_name2} уже существует")
        else:
            result = conn.eval(f"""
               local space = box.schema.space.create('{space_name2}', {{
                   if_not_exists = true,
                   format = {{
                       {{name = 'key', type = 'string'}},
                       {{name = 'value', type = 'varbinary'}},
                   }}
               }})
               return true
           """)

            print(f"Пространство {space_name2} создано")

    except Exception as e:
        print(f"Ошибка создания: {e}")
