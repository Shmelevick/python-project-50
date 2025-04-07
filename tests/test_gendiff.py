import json
import os

from gendiff import generate_diff


def test_flat_json():
    file1_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file1.json')
    file2_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file2.json')
    expected_result_1 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_1.txt')

    with open(expected_result_1, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file1_path, file2_path) == expected_result


def test_flat_bigger_json():
    file3_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file3.json')
    file4_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file4.json')
    expected_result_2 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_2.txt')

    with open(expected_result_2, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file3_path, file4_path) == expected_result


def test_flat_yaml():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_result_flat_yaml = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml_flat.txt')

    with open(expected_result_flat_yaml, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file5_path, file6_path, 'plain') == expected_result


def test_nested_yaml():
    file7_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file7.yml')
    file8_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file8.yml')
    expected_result_4 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_4.txt')

    with open(expected_result_4, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file7_path, file8_path) == expected_result


def test_nested_json():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_4.txt')

    with open(expected_result, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file9_path, file10_path) == expected_result


def test_plain_yaml_nested():
    file7_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file7.yml')
    file8_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file8.yml')
    expected_plain_yaml = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_plain_yaml.txt')

    with open(expected_plain_yaml, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file7_path, file8_path, 'plain') == expected_result


def test_plain_yaml_flat():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_plain_yaml_flat = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml_flat.txt')

    with open(expected_plain_yaml_flat, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file5_path, file6_path, 'plain') == expected_result


def test_plain_json_nested():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result_nested = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml.txt')

    with open(expected_result_nested, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file9_path, file10_path, 'plain') == expected_result


def test_json_to_json_nested():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result_json = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_json.json')

    with open(expected_result_json, encoding='utf-8') as file:
        expected_result = json.load(file)

    result_json_str = generate_diff(file9_path, file10_path, 'json')
    actual_result = json.loads(result_json_str)

    assert actual_result == expected_result


def test_flat_yaml_to_json():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_result_flat_yaml = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_flat_yaml.json')

    with open(expected_result_flat_yaml, encoding='utf-8') as file:
        expected_result = json.load(file)

    result_json_str = generate_diff(file5_path, file6_path, 'json')
    actual_result = json.loads(result_json_str)

    assert actual_result == expected_result
