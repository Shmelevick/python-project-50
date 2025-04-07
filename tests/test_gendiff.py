import json
import os

import yaml

from gendiff import generate_diff


def test_flat_json():
    file1_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file1.json')
    file2_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file2.json')
    expected_result_1 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_1.txt')

    with open(file1_path, encoding='utf-8') as file:
        file1 = json.load(file)

    with open(file2_path, encoding='utf-8') as file:
        file2 = json.load(file)

    with open(expected_result_1, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file1, file2) == expected_result


def test_flat_bigger_json():
    file3_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file3.json')
    file4_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file4.json')
    expected_result_2 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_2.txt')

    with open(file3_path, encoding='utf-8') as file:
        file3 = json.load(file)

    with open(file4_path, encoding='utf-8') as file:
        file4 = json.load(file)

    with open(expected_result_2, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file3, file4) == expected_result


def test_flat_yaml():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_result_flat_yaml = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml_flat.txt')

    with open(file5_path, encoding='utf-8') as file:
        file5 = yaml.safe_load(file)

    with open(file6_path, encoding='utf-8') as file:
        file6 = yaml.safe_load(file)

    with open(expected_result_flat_yaml, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file5, file6, 'plain') == expected_result


def test_nested_yaml():
    file7_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file7.yml')
    file8_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file8.yml')
    expected_result_4 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_4.txt')

    with open(file7_path, encoding='utf-8') as file:
        file7 = yaml.safe_load(file)

    with open(file8_path, encoding='utf-8') as file:
        file8 = yaml.safe_load(file)

    with open(expected_result_4, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file7, file8) == expected_result


def test_nested_json():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_4.txt')

    with open(file9_path, encoding='utf-8') as file:
        file9 = json.load(file)

    with open(file10_path, encoding='utf-8') as file:
        file10 = json.load(file)

    with open(expected_result, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file9, file10) == expected_result


def test_plain_yaml_nested():
    file7_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file7.yml')
    file8_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file8.yml')
    expected_plain_yaml = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_plain_yaml.txt')

    with open(file7_path, encoding='utf-8') as file:
        file7 = yaml.safe_load(file)

    with open(file8_path, encoding='utf-8') as file:
        file8 = yaml.safe_load(file)

    with open(expected_plain_yaml, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file7, file8, 'plain') == expected_result


def test_plain_yaml_flat():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_plain_yaml_flat = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml_flat.txt')

    with open(file5_path, encoding='utf-8') as file:
        file5 = yaml.safe_load(file)

    with open(file6_path, encoding='utf-8') as file:
        file6 = yaml.safe_load(file)

    with open(expected_plain_yaml_flat, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file5, file6, 'plain') == expected_result


def test_plain_json_nested():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result_nested = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_plain_yaml.txt')

    with open(file9_path, encoding='utf-8') as file:
        file9 = json.load(file)

    with open(file10_path, encoding='utf-8') as file:
        file10 = json.load(file)

    with open(expected_result_nested, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file9, file10, 'plain') == expected_result


def test_json_to_json_nested():
    file9_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file9.json')
    file10_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file10.json')
    expected_result_json = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_json.json')

    with open(file9_path, encoding='utf-8') as file:
        file9 = json.load(file)

    with open(file10_path, encoding='utf-8') as file:
        file10 = json.load(file)

    with open(expected_result_json, encoding='utf-8') as file:
        expected_result = json.load(file)

    result_json_str = generate_diff(file9, file10, 'json')
    actual_result = json.loads(result_json_str)

    assert actual_result == expected_result


def test_flat_yaml_to_json():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_result_flat_yaml = os.path.join(os.path.dirname(__file__),
    'test_data', 'expected_flat_yaml.json')

    with open(file5_path, encoding='utf-8') as file:
        file5 = yaml.safe_load(file)

    with open(file6_path, encoding='utf-8') as file:
        file6 = yaml.safe_load(file)

    with open(expected_result_flat_yaml, encoding='utf-8') as file:
        expected_result = json.load(file)

    result_json_str = generate_diff(file5, file6, 'json')
    actual_result = json.loads(result_json_str)

    assert actual_result == expected_result