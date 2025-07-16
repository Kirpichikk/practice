"""
нужно написать функцию поиска по составному запросу

"""

from connection import Connection

conn = Connection()

conn.eval(f"""
    function select_rows(space_name, column_name, ...)
        local options = ...
        if type(options) ~= "table" then
            options = {{}}
        end
        
        local limit = options.limit or 100000  -- Лимит по умолчанию
        local offset = options.offset
        
        local space = box.space[space_name]
        
        local data = {{}}
        local count = 0
        
        local format = space:format()
        
        local index_column = {{}}
        
        for _,name in ipairs(column_name) do
            for i, tuple in ipairs(format) do
                if tuple.name == name then
                    table.insert(index_column, i)
                    break
                end
            end
        end
        
        for _, tuple in space:pairs(nil,{{after = offset}}) do
            if count >= limit then
                break
            end
            
            local rows = {{}}
            for _, row_name in ipairs(index_column) do
                table.insert(rows, tuple[row_name])
            end
            table.insert(data, rows)
            count = count + 1
        end
        return data
    end
""")

conn.eval(f"""
    function select_with_value(space_name, index_name, value, ...)
        local options = ...
        if type(options) ~= "table" then
            options = {{}}
        end
        
        local iterator_val = options.iterator or "EQ"
        local limit_val = options.limit or 100000
        local offset_val = options.offset
        local after_val = options.after
        local fetch_pos_val = options.fetch_pos
        
        local data = {{}}
        
        local index = box.space[space_name].index[index_name]
        
        data = index:select({{value}}, {{iterator = iterator_val, limit = limit_val, after = after_val, fetch_pos = fetch_pos_val, offset = offset_val}})
        
        return data
    end
""")

conn.eval("""
    function select_with_values(space_name, index_name, value1, value2, options)
        options = options or {}

        -- Получаем пространство и индекс
        local space = box.space[space_name]
        if not space then
            error(string.format("Space '%s' not found", space_name))
        end

        local index = space.index[index_name]
        if not index then
            error(string.format("Index '%s' not found in space '%s'", index_name, space_name))
        end

        -- Формируем ключ поиска в зависимости от наличия второго значения
        local search_key = {value1, value2}

        -- Параметры запроса
        local query_options = {
            iterator = options.iterator,
            limit = options.limit or 100000,
            offset = options.offset,
            after = options.after,
            fetch_pos = options.fetch_pos,
            partial = options.partial
        }

        -- Выполняем запрос
        return index:select(search_key, query_options)
    end
""")