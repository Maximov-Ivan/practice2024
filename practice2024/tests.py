import pandas as pd
import json
from django.test import TestCase
from .modules import load_json, get_properties, get_subsets, group_by_len, list_to_df, write_csv
from .brute import brute
from .optimized import optimized
from .app import main


# тесты для функции load_json файла modules.py
class LoadJsonTestCase(TestCase):
    def test_load_json(self):
        json_string = '[{"a": 0, "b": 1}, {"b": 2, "c": 3}]'
        self.assertEqual(load_json(json_string), [{'a': 0, 'b': 1}, {'b': 2, 'c': 3}])


# тесты для функции get_properties файла modules.py
class GetPropertiesTestCase(TestCase):
    def test_get_properties(self):
        objects = [{'a': 0, 'b': 1}, {'b': 2, 'c': 3}]
        self.assertEqual(get_properties(objects), (['a', 'b', 'c'], 3))


# тесты для функции get_subsets файла modules.py
class GetSubsetsTestCase(TestCase):
    def test_get_subsets(self):
        properties = ['a', 'b', 'c']
        self.assertEqual(get_subsets(properties), [['a', 'b', 'c'], ['a', 'b'], ['a', 'c'], ['b', 'c'], ['a'], ['b'], ['c']])


# тесты для функции group_by_len файла modules.py
class GroupByLenTestCase(TestCase):
    def test_group_by_len(self):
        subsets = [['a', 'b', 'c'], ['a', 'b'], ['a', 'c'], ['b', 'c'], ['a'], ['b'], ['c']]
        m = 3
        self.assertEqual(group_by_len(subsets, m), [[], [['a'], ['b'], ['c']], [['a', 'b'], ['a', 'c'], ['b', 'c']], [['a', 'b', 'c']]])


# тесты для функции list_to_df файла modules.py
class ListToDfTestCase(TestCase):
    def test_list_to_df(self):
        lst = ['a', 'c']
        self.assertEqual(list_to_df(lst).equals(pd.DataFrame(['a', 'c'])), True)


# тесты для функции write_csv файла modules.py
class WriteCsvTestCase(TestCase):
    def test_write_csv(self):
        df = pd.DataFrame(['a', 'c'])
        self.assertEqual(write_csv(df), 'a\r\nc\r\n')


# тесты для функции brute файла brute.py
class BruteTestCase(TestCase):
    def test_brute(self):
        json_string = '[{"a": 0, "b": 1, "c": 0}, {"a": 0, "b": 2, "c": 3}, {"b": 3, "c": 3}]'
        self.assertEqual(brute(json_string), 'b\r\n')


# тесты для функции optimized файла optimized.py
class OptimizedTestCase(TestCase):
    def test_optimized(self):
        json_string = '[{"a": 0, "b": 1, "c": 0}, {"a": 0, "b": 2, "c": 3}, {"b": 3, "c": 3}]'
        self.assertEqual(optimized(json_string), 'b\r\n')


# тесты для функции main файла app.py
class MainTestCase(TestCase):
    def test_main(self):
        json_string = '[{"a": 0, "b": 1, "c": 0}, {"a": 0, "b": 2, "c": 3}, {"b": 3, "c": 3}]'
        self.assertEqual(main(json_string), 'b\r\n')
        json_string = json.dumps(json.load(open('example.json', 'r', encoding='utf-8')))
        self.assertEqual(main(json_string), 'about\r\n')
        json_string = json.dumps(json.load(open('example_without_about.json', 'r', encoding='utf-8')))
        self.assertEqual(main(json_string), 'видДеятельности\r\nимя\r\nкласс\r\nподгруппа\r\nпредмет\r\n')
        json_string = json.dumps(json.load(open('test1.json', 'r', encoding='utf-8')))
        self.assertEqual(main(json_string), '0\r\n1\r\n2\r\n')
