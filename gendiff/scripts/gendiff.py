import argparse
import json

import yaml

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
        return [[key, value] for key, value in value.items()]
    elif value is None:
        return 'null'
    return value



def get_diff_plain(file1, file2):
    result = []

    keys1 = get_key(file1)
    keys2 = get_key(file2)
    all_keys = sorted(keys1 | keys2)

    for key in all_keys:
        result.append(key)

        val1 = file1.get(key) if isinstance(file1, dict) else None
        val2 = file2.get(key) if isinstance(file2, dict) else None

        if isinstance(val1, dict) and isinstance(val2, dict):
            result.append(get_diff_plain(val1, val2))
        else:
            if val1 == val2:
                result.append(format_value_plain(val1))
            else:
                if key in keys1:
                    result.append('- ' + str(format_value_plain(val1)))
                if key in keys2:
                    result.append('+ ' + str(format_value_plain(val2)))

    return result



def generate_diff(file1: dict, file2: dict, format_name='stylish') -> str:
    ''' Finds difference in two dicts and returns it as a formatted string '''
    return (
        get_diff_string(file1, file2)
        if format_name == 'NOT_stylish'
        else get_diff_plain(file1, file2)
    )


def load_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_yaml_yml(file_path):
    with open(file_path, encoding='utf-8') as f:
        return yaml.safe_load(f)


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

    print(generate_diff(first_data, second_data))

    # print(args)


if __name__ == '__main__':
    main()