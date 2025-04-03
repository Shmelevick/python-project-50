import argparse
import json

import yaml


def generate_diff(file1: dict, file2: dict, level=0) -> str:
    ''' Finds difference in two dicts and returns it as a formatted string '''
    
    def format_value(value, level):
        """ Format values: bool -> lowercase, None -> null, dict -> formatted """
        if value is None:
            print(f'>{value}<')

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
        lines = [f'{ind * (level + 2)}{key}: {format_value(val, level + 2)}' for key, val in d.items()]
        return f'{{\n' + '\n'.join(lines) + f'\n{ind * (level)}}}'

    ind = '  '
    result = '{\n'

    keys1 = set(file1.keys()) if isinstance(file1, dict) else set()
    keys2 = set(file2.keys()) if isinstance(file2, dict) else set()
    all_keys = sorted(keys1 | keys2)

    for key in all_keys:
        val1 = file1.get(key) if isinstance(file1, dict) else None
        val2 = file2.get(key) if isinstance(file2, dict) else None

        if isinstance(val1, dict) and isinstance(val2, dict):
            result += f'{ind * (level + 2)}{key}: {generate_diff(val1, val2, level + 2)}\n'
        else:
            if val1 == val2:
                result += f'{ind * (level + 2)}{key}: {format_value(val1, level + 2)}\n'
            else:
                if key in keys1:
                    result += f'{ind * (level + 1)}- {key}: {format_value(val1, level + 2)}\n'
                if key in keys2:
                    result += f'{ind * (level + 1)}+ {key}: {format_value(val2, level + 2)}\n'

    result += f'{ind * (level)}}}'

    with open("result_diff_output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(result)
    return result


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