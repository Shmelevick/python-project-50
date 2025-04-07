from .make_list_from_file import get_key, get_list  # noqa: F401


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
            nxt_key.endswith(key[2:])
            and (key.startswith('-')
            and nxt_key.startswith('+'))
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
        if value1 in ('null', 'true', 'false', cv, '0', 0)
        else f"'{value1}'"
    )
    value2 = (
        value2
        if value2 in ('null', 'true', 'false', cv, '0', 0)
        else f"'{value2}'"
    )

    return (
        f"Property '{address}{key.removeprefix('- ')}' was updated. "
        f"From {value1} to {value2}\n"
    )


def _operate_add_remove(key, value, address):
    cv = '[complex value]'

    value = cv if isinstance(value, list) else value
    value = (
        value
        if value in ('null', 'true', 'false', '0', 0, cv)
        else f"'{value}'"
    )

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