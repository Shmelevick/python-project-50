
def get_key(file):
    return set(file.keys()) if isinstance(file, dict) else set()


def get_list(file1, file2):
    result = []

    keys1 = get_key(file1)
    keys2 = get_key(file2)
    all_keys = sorted(keys1 | keys2)

    for key in all_keys:

        val1 = file1.get(key) if isinstance(file1, dict) else None
        val2 = file2.get(key) if isinstance(file2, dict) else None

        if isinstance(val1, dict) and isinstance(val2, dict):
            result.append(key)
            result.append(get_list(val1, val2))
        else:
            if val1 == val2:
                result.append(str(key))
                result.append(format_value_plain(val1))
            else:
                if key in keys1:
                    result.append('- ' + str(key)) 
                    result.append(format_value_plain(val1))
                if key in keys2:
                    result.append('+ ' + str(key)) 
                    result.append(format_value_plain(val2))

    return result


def format_value_plain(value):

    if isinstance(value, bool):
        return str(value).lower()
    elif value is None and isinstance(value, str):
        return ' '
    elif isinstance(value, dict):
        result = []
        for key, val in value.items():
            result.append(key)
            result.append(format_value_plain(val))
        return result
    elif value is None:
        return 'null'
    return value