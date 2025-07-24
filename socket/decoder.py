import struct

# Определение флагов
FLAG_INSERT = 128  # Сообщение содержит данные для вставки
FLAG_QUERY = 0  # Сообщение содержит запрос на поиск


def parse_single_message(data):
    # Минимальный размер заголовка
    if len(data) < 4:
        return None, None, None, data

    # Извлекаем заголовок ключа
    key_header = data[:4]
    key_header_val = struct.unpack('>I', key_header)[0]

    # Извлекаем флаги и реальную длину ключа
    flags = (key_header_val >> 24) & 0xFF
    real_key_length = key_header_val & 0x00FFFFFF


    # Проверяем доступность данных для ключа
    if len(data) < 4 + real_key_length:
        return None, None, None, data
    if flags == FLAG_QUERY:
    # Извлекаем ключ
        key_start = 4
        key_end = key_start + real_key_length
        key_bytes = data[key_start:key_end]

    # Для сообщений с флагом INSERT проверяем наличие заголовка значения
        value_bytes = b''
        value_length = 0
        remaining_start = key_end

    # Если установлен флаг INSERT, ожидаем заголовок значения
    if flags == FLAG_INSERT:
        if len(data) < 8:
            return None, None, None, data

        value_header = data[4:8]
        value_length = struct.unpack('>I', value_header)[0]

        # Проверяем доступность данных
        remaining_start = 8 + real_key_length + value_length
        if len(data) < remaining_start:
            return None, None, None, data

        # Извлекаем ключ
        key_start = 8
        key_end = key_start + real_key_length
        key_bytes = data[key_start:key_end]

        # Извлекаем значение (если оно есть)
        value_bytes = b''
        if value_length > 0:
            value_start = key_end
            value_end = value_start + value_length
            value_bytes = data[value_start:value_end]

    # Декодируем ключ
    try:
        key = key_bytes.decode()
    except UnicodeDecodeError:
        key = key_bytes

    # Декодируем значение (если оно есть)
    value = None
    if value_bytes:
        try:
            value = value_bytes.decode()
        except UnicodeDecodeError:
            value = value_bytes

    # Возвращаем результат + оставшиеся данные
    return flags, key, value, data[remaining_start:]


def handle_message(flags, key, value, conn):
    """Обработка сообщения в зависимости от флагов"""
    if flags == FLAG_INSERT:
        print(f"[INSERT] Вставка данных: Ключ={key}, Значение={value}")
        result = conn.upsert('cache1', (key, value),[('=', 1, value)])
        return ["success"]

    elif flags == FLAG_QUERY:
        print(f"[QUERY] Поиск данных по ключу: {key}")
        result = conn.call('select_with_value', ('cache1', 'cache1_key', key))

        if result:
            return result[0][0]
        else:
            return key



def process_message_stream(data_stream, conn):
    """Обработка потока сообщений"""
    remaining_data = data_stream
    results = []

    while True:
        flags, key, value, remaining_data = parse_single_message(remaining_data)

        # Если сообщение неполное, выходим
        if flags is None:
            break

        # Обрабатываем сообщение
        result = handle_message(flags, key, value, conn)
        results.append(result)

    return results