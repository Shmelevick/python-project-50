import argparse
import json

import yaml

from .json_gendiff import json_format_diff
from .plain_gendiff import get_list, plain_format_diff
from .stylish_gendiff import get_diff_string


def generate_diff(file1: dict, file2: dict, format_name='stylish') -> str:
    ''' Finds difference in two dicts and returns it as a formatted string '''
    match format_name:
        case 'stylish':
            return get_diff_string(file1, file2)
        case 'plain':
            return plain_format_diff(get_list(file1, file2)).strip()
        case 'json':
            return json_format_diff(file1, file2)


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

    parser.add_argument('first_file', type=str)
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
