import argparse
import json


def generate_diff(file1: dict, file2: dict) -> str:
    
    ''' Finds difference in two dicts'''

    def format_bool(value):
        """ Bool True/False -> str true/false"""
        if isinstance(value, bool):
            return str(value).lower()
        return value

    cont_list = sorted([x for x in file1 | file2])
    result = '{\n'

    for key in cont_list:
        val1 = file1.get(key)
        val2 = file2.get(key)

        if val1 == val2:
            result += f'    {key}: {format_bool(val1)}\n'
        elif key in file1 and key in file2:
            result += f'  - {key}: {format_bool(val1)}\n'
            result += f'  + {key}: {format_bool(val2)}\n'
        elif key in file1:
            result += f'  - {key}: {format_bool(val1)}\n'
        elif key in file2:
            result += f'  + {key}: {format_bool(val2)}\n'
        else:
            return f'Error: {key}'

    return result + '}'





def load_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )

    parser.add_argument('first_file', type=str) # help='Path to the first file'
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output',
                        default='stylish', choices=['stylish', 'plain', 'json'])
    args = parser.parse_args()

    first_data = load_json(args.first_file)
    second_data = load_json(args.second_file)

    print(generate_diff(first_data, second_data))

    # print(args)


if __name__ == '__main__':
    main()