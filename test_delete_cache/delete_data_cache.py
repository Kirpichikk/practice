
def delete_data(conn, space_name, key):
    for i in key:
        space = conn.call(f"box.space.{space_name}:get", (i,))
        if space:
            delete_result = conn.call(
                f"box.space.{space_name}:delete",
                (key,)
            )
            return delete_result
        else:
            return "нет возможности удаления по данному ключу"