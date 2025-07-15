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

def get_data(data):
    match data['Code']:
        case 263:
            return data['Data']
        case 8:
            return tuple(data['Data'].split("."))
        case 443:
            match data['Data']['Subscription-Id-Type']['Data']:
                case 0 | 1 | 2:
                    return data['Data']['Subscription-Id-Data']['Data']
                case _:
                    return None
        case _:
            return False

# Пример использования
def creation_data(pack = False):
    file_path = [r"D:\downloads\CCR-U_p0_v0.json",r"D:\downloads\CCR-U_p0_v1.json",r"D:\downloads\CCR-U_p0_v2.json"]
    result_AVP = []
    final_result = []
    try:
        for path in file_path:
            result = json_file_to_array(path)
            for i in result:
                result_AVP.append(i["AVP"])

        for i in result_AVP:
            pre_final = []
            for j in i:
                data = get_data(j)
                if data != False:
                    pre_final.append(data)

            pre_final.insert(-1, None)
            pre_final.append(None)
            pre_final.append(pre_final[0])
            if pack == True: pre_final.insert(0, None)

            final_result.append(tuple(pre_final))

        final_result = final_result * 3333 + final_result[0:10]

        return final_result

    except Exception as e:
        print(f"Ошибка: {e}")
