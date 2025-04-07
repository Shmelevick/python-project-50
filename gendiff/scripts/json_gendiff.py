import json

from .make_list_from_file import get_list


def jsonify_list(data_list: list) -> str:

    def inner(inner_data):
        result = {}

        for key, value in zip(inner_data[::2], inner_data[1::2]):

            if isinstance(value, list):
                result[key] = inner(value)

            else:
                match value:
                    case 'false':
                        result[key] = False
                    case 'true':
                        result[key] = True
                    case 'null':
                        result[key] = None
                    case _:
                        result[key] = value

# A comment for myself:
# mapping = {'false': False, 'true': True, 'null': None}
# result[key] = mapping.get(value, value)

        return result

    return json.dumps(inner(data_list), indent=2)


def json_format_diff(file1, file2):
    return jsonify_list(get_list(file1, file2))