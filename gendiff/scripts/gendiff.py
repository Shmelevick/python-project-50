import json, argparse, yaml


IND = '  '


def format_value(value, level=None):
    """Format values: bool -> lowercase, None -> null, dict -> formatted"""

    if isinstance(value, bool):
        return str(value).lower()
    elif value is None and isinstance(value, str):
        return ' '
    elif isinstance(value, dict):
        return format_dict(value, level)
    elif value is None:
        return 'null'
    return value


def format_dict(d, level):
    """ Properly formats nested dicts """
    lines = [
        f'{IND * (level + 2)}{key}: {format_value(val, level + 2)}'
        for key, val
        in d.items()
        ]

    return '{\n' + '\n'.join(lines) + f'\n{IND * (level)}}}'


def get_key(file):
    return set(file.keys()) if isinstance(file, dict) else set()


def get_diff_string(file1: dict, file2: dict, level=0):
    result = '{\n'

    keys1 = get_key(file1)
    keys2 = get_key(file2)
    all_keys = sorted(keys1 | keys2)

    for key in all_keys:
        val1 = file1.get(key) if isinstance(file1, dict) else None
        val2 = file2.get(key) if isinstance(file2, dict) else None

        if isinstance(val1, dict) and isinstance(val2, dict):
            result += (
                f'{IND * (level + 2)}{key}: '
                f'{get_diff_string(val1, val2, level + 2)}\n'
            )
        else:
            if val1 == val2:
                result += (
                    f'{IND * (level + 2)}{key}: '
                    f'{format_value(val1, level + 2)}\n'
                )
            else:
                if key in keys1:
                    result += (
                        f'{IND * (level + 1)}- {key}: '
                        f'{format_value(val1, level + 2)}\n'
                    )
                if key in keys2:
                    result += (
                        f'{IND * (level + 1)}+ {key}: '
                        f'{format_value(val2, level + 2)}\n'
                    )
    result += f'{IND * (level)}}}'
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


def get_diff_plain(file1, file2):
    result = []

    keys1 = get_key(file1)
    keys2 = get_key(file2)
    all_keys = sorted(keys1 | keys2)

    for key in all_keys:

        val1 = file1.get(key) if isinstance(file1, dict) else None
        val2 = file2.get(key) if isinstance(file2, dict) else None

        if isinstance(val1, dict) and isinstance(val2, dict):
            result.append(key)
            result.append(get_diff_plain(val1, val2))
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


def plain_format_diff(data, address='', result=''):

    for i, (key, value) in enumerate(zip(data[::2], data[1::2])):
        if _key_already_processed(key, result):
            continue

        if isinstance(value, list):
            result += plain_format_diff(value, f'{address}{key}.')

        nxt_key = None if not i + 1 < len(data) / 2 else data[2 * (i + 1)]

        if not nxt_key:
            if key.startswith(('+', '-')):
                result += _operate_add_remove(key, value, address)
            continue

        if nxt_key.endswith(key[2:]) and (key.startswith('-') and nxt_key.startswith('+')):
            result += _operate_update(key, value, data[2 * (i + 1) + 1], address)

        elif key.startswith(('+', '-')):
            result += _operate_add_remove(key, value, address)

    return result


def _operate_update(key, value1, value2, address):
    cv = '[complex value]'

    value1 = cv if isinstance(value1, list) else value1
    value2 = cv if isinstance(value2, list) else value2
    value1 = value1 if value1 in ('null', 'true', 'false', cv) else f"'{value1}'"
    value2 = value2 if value2 in ('null', 'true', 'false', cv) else f"'{value2}'"

    return f"Property '{address}{key.removeprefix('- ')}' was updated. From {value1} to {value2}\n"


def _operate_add_remove(key, value, address):
    cv = '[complex value]'

    value = cv if isinstance(value, list) else value
    value = value if value in ('null', 'true', 'false', cv) else f"'{value}'"

    if key.startswith('+'):
        return f"Property '{address}{key.removeprefix('+ ')}' was added with value: {value}\n"
    if key.startswith('- '):
        return f"Property '{address}{key.removeprefix('- ')}' was removed\n"


def _key_already_processed(raw_key, result):
    if len(result) < 2:
        return False
    key = raw_key.lstrip('+ ').lstrip('- ')
    return key in result.split('\n')[-2]


def generate_diff(file1: dict, file2: dict, format_name='stylish') -> str:
    ''' Finds difference in two dicts and returns it as a formatted string '''
    match format_name:
        case 'stylish':
            return get_diff_string(file1, file2)
        case 'plain':
            return plain_format_diff(get_diff_plain(file1, file2))
    

def load_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_yaml_yml(file_path):
    with open(file_path, encoding='utf-8') as f:
        return yaml.safe_load(f)


# print(get_diff_plain(
#     load_yaml_yml('tests/test_data/file7.yaml'),
#     load_yaml_yml('tests/test_data/file8.yaml'))
#     )


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )

    parser.add_argument('first_file', type=str)  # help='Path to the first file'
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output',
    default='stylish', choices=['stylish', 'plain', 'json'])

    args = parser.parse_args()
    arg1 = args.first_file
    arg2 = args.second_file
    format_type = args.format

    first_data = (
        load_yaml_yml(arg1)
        if arg1.endswith(('yml', 'yaml'))
        else load_json(arg1)
    )

    second_data = (
        load_yaml_yml(arg2) 
        if arg2.endswith(('yml', 'yaml'))
        else load_json(arg2)
    )

    print(generate_diff(first_data, second_data, format_name=format_type))

    print(args)


if __name__ == '__main__':
    main()


# def plain_format_diff(data, address='', result=''):

#     for i, (key, value) in enumerate(zip(data[::2], data[1::2])):
#         if isinstance(value, list):
#             result += plain_format_diff(value, f'{address}{key}.')

#         if i + 1 < len(data) // 2:
#             nxt_key = data[2 * (i + 1)]
#             if nxt_key.endswith(key[2:]) and (key.startswith('-') and nxt_key.startswith('+')):
#                 result += _operate_update(key, value, data[2 * (i + 1) + 1], address)


#             elif key.startswith(('+', '-')):
#                 result += _operate_add_remove(key, value, address)

#     return result


# def _operate_update(key, value1, value2, address):
#     return f"Property '{address}{key.lstrip('- ')}' was updated. From {value1} to {value2}\n"


# def _operate_add_remove(key, value, address):
#     if key.startswith('+'):
#         return f"Property '{address}{key.lstrip('+ ')}' was added with value: {value}\n"
#     if key.startswith('- '):
#         return f"Property '{address}{key.lstrip('- ')}' was removed\n"
    
#     def plain_format_diff(data, address='', result=[]):
#     if not data:
#         return result

#     for i, (key, value) in enumerate(zip(data[::2], data[1::2])):
#         if result and key[2:] in result[-1].split()[1]:
#             continue

#         if isinstance(value, list):
#             result.append(plain_format_diff(value, f'{address}{key}.'))
#             break

#         elif i + 1 < len(data) // 2:
#             nxt_key = data[2 * (i + 1)]

#             if nxt_key.endswith(key[2:]) and (key.startswith('-') and nxt_key.startswith('+')):
#                 result.append(_operate_update(key, value, data[2 * (i + 1) + 1], address))

#             elif key.startswith(('+', '-')):
#                 result.append(_operate_add_remove(key, value, address))

#         continue


#     return ''.join(result)