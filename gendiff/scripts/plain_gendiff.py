def get_key(file):
    return set(file.keys()) if isinstance(file, dict) else set()


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

        if (
            nxt_key.endswith(key[2:]) and
            (key.startswith('-') and
            nxt_key.startswith('+'))
        ):
            result += _operate_update(
                key,
                value,
                data[2 * (i + 1) + 1],
                address
            )

        elif key.startswith(('+', '-')):
            result += _operate_add_remove(key, value, address)

    return result


def _operate_update(key, value1, value2, address):
    cv = '[complex value]'

    value1 = cv if isinstance(value1, list) else value1
    value2 = cv if isinstance(value2, list) else value2
    value1 = (
        value1
        if value1 in ('null', 'true', 'false', cv)
        else f"'{value1}'"
    )
    value2 = (
        value2
        if value2 in ('null', 'true', 'false', cv)
        else f"'{value2}'"
    )

    return (
        f"Property '{address}{key.removeprefix('- ')}' was updated. "
        f"From {value1} to {value2}\n"
    )


def _operate_add_remove(key, value, address):
    cv = '[complex value]'

    value = cv if isinstance(value, list) else value
    value = value if value in ('null', 'true', 'false', cv) else f"'{value}'"

    if key.startswith('+'):
        return (
            f"Property '{address}{key.removeprefix('+ ')}' "
            f"was added with value: {value}\n")
    if key.startswith('- '):
        return (
            f"Property '{address}{key.removeprefix('- ')}' was removed\n")
    return None


def _key_already_processed(raw_key, result):
    if len(result) < 2:
        return False
    key = raw_key.lstrip('+ ').lstrip('- ')
    return key in result.split('\n')[-2]