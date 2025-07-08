from connection import Connection

conn = Connection()

conn.eval(f"""
    fiber = require('fiber')

    function insert_batch(batch)
        fiber.create(function(data)
            for _, tuple in ipairs(data) do
                local id = box.sequence.id_seq:next()
                box.space.users:insert({{id, tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7]}})
                fiber.sleep(0)
            end
            print("Batch inserted, size:", #data)
        end, batch)
        return "Insertion started"
    end
""")