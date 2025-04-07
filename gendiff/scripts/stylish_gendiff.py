IND = '  '


def get_key(file):
    return set(file.keys()) if isinstance(file, dict) else set()


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


# def get_key(file):
#     return set(file.keys()) if isinstance(file, dict) else set()


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