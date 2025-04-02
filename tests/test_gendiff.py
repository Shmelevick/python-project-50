import json
import os

import yaml

from gendiff import generate_diff


def test_flat_yaml():
    file5_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file5.yaml')
    file6_path = os.path.join(os.path.dirname(__file__), 'test_data',
    'file6.yaml')
    expected_result_3 = os.path.join(os.path.dirname(__file__), 'test_data',
    'expected_result_3.txt')

    with open(file5_path, encoding='utf-8') as file:
        file5 = yaml.safe_load(file)

    with open(file6_path, encoding='utf-8') as file:
        file6 = yaml.safe_load(file)

    with open(expected_result_3, encoding='utf-8') as file:
        expected_result = file.read()

    assert generate_diff(file5, file6) == expected_result


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
        expected_result_2 = file.read()

    assert generate_diff(file3, file4) == expected_result_2