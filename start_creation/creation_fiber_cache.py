from connection import Connection

conn = Connection()

conn.eval("""
    fiber = require('fiber')

    local wait_channel = fiber.channel()

    completed_batches = 0
    total_batches = 0

    -- Функция вставки одного пакета
    function insert_batch_cache1(batch)
        total_batches = total_batches + 1
        fiber.create(function(data)
            for _, tuple in ipairs(data) do
                box.space.cache1:insert{tuple[1], 
                                      tuple[2]}
            end
            completed_batches = completed_batches + 1
            wait_channel:put(true)
        end, batch)
        return "Insertion started"
    end

    function insert_batch_cache2(batch)
        total_batches = total_batches + 1
        fiber.create(function(data)
            for _, tuple in ipairs(data) do
                box.space.cache2:insert{tuple[1], 
                                      tuple[2]}
            end
            completed_batches = completed_batches + 1
            wait_channel:put(true)
        end, batch)
        return "Insertion started"
    end

    function wait_completion()
        while completed_batches < total_batches do
            fiber.sleep(0.1)
        end
        return true
    end
""")