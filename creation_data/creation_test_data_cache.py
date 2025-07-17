import json
import base64

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

def get_data(data):
    match data['Code']:
        case 263 | 8:
            return data['Data']
        case 443:
            match data['Data']['Subscription-Id-Type']['Data']:
                case 0 | 1 | 2:
                    return data['Data']['Subscription-Id-Data']['Data']
                case _:
                    return None
        case _:
            return False

# Пример использования
def creation_data(cache):
    path = r"D:\data.json"
    final_result = []
    try:
        result = json_file_to_array(path)

        match cache:
            case 1:
                key = 0
                for i in result:
                    final_result.append((str(key),i['SessId']))
                    key += 1
                return final_result
            case 2:
                key = 0
                for i in result:
                    final_result.append((str(key), base64.b64decode(i['ReqAns']['$binary']['base64'])))
                    key += 1
                return final_result

    except Exception as e:
        print(f"Ошибка: {e}")

print(creation_data(2)[0])