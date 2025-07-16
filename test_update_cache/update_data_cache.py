
def update_value(conn, space_name, key, new_value):
    for i in key:
        space = conn.call(f"box.space.{space_name}:get", (i,))
        if space:
            update_result = conn.call(
                f"box.space.{space_name}:update",
                (key, [("=", "value", new_value)])  # Исправлено здесь
            )
            return update_result
        else:
            return "нет возможности вставки по данному ключу"

