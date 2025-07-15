import json


def json_file_to_array(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

            # Попытка 1: Обработка как единый JSON
            try:
                data = json.loads(content)
                return data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                pass

            # Попытка 2: Обработка как JSON Lines (построчно)
            data = []
            lines = content.splitlines()
            for line in lines:
                if line.strip():
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Ошибка в строке: {line[:30]}...: {e}")
            return data

    except FileNotFoundError:
        raise ValueError(f"Файл не найден: {file_path}")
    except Exception as e:
        raise ValueError(f"Ошибка обработки: {e}")


# Пример использования
if __name__ == "__main__":
    file_path = r"D:\data.json"
    try:
        result = json_file_to_array(file_path)
        print(f"Успешно загружено {len(result)} элементов")
        print(f"Первый элемент: {result[0] if result else 'нет данных'}")
    except Exception as e:
        print(f"Ошибка: {e}")