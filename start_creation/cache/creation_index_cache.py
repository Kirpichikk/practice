from connection import Connection

space_name1 = "cache1"
space_name2 = "cache2"

conn = Connection()

if conn:
    try:
        conn.eval(f"""
            box.space.{space_name1}:create_index('{space_name1}_key', {{
                parts = {{'key'}},
            }})
            
            box.space.{space_name2}:create_index('{space_name2}_key', {{
                parts = {{'key'}},
            }})
        """)

    except Exception as e:
        print(f"Ошибка создания: {e}")