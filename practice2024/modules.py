import json
import pandas as pd


# функция для чтения формата json
# на вход принимает json-строку
# возвращает объект Python (обычно список или словарь,
# в зависимости от структуры входной строки)
def load_json(json_string):
    objects = json.loads(json_string)
    return objects


# функция для получения списка возможных признаков сущностей
# на вход принимает набор сущностей
# возвращает список возможных признаков
def get_properties(objects):
    properties = set()
    for object in objects:
        for property in object.keys():
            properties.add(property)
    properties = sorted(list(properties))
    m = len(properties)
    return properties, m


# функция для получения списка всех комбинаций признаков
# на вход принимает список признаков
# возвращает список комбинаций
def get_subsets(properties):
    m = len(properties)
    subsets = list()
    for i in range(1, 1 << m):
        subset = [properties[j] for j in range(m) if (i & (1 << j))]
        subsets.append(sorted(subset))
    subsets.sort(key=len, reverse=True)
    return subsets


# функция для группировки списка комбинаций признаков по длине
# на вход принимает список комбинаций
# возвращает список, состоящий из списков комбинаций одинаковой длины
def group_by_len(subsets, m):
    grouped_subsets = [[] for i in range(m + 1)]
    for subset in subsets:
        grouped_subsets[len(subset)].append(subset)
    return grouped_subsets


# функция для перевода списка в DataFrame
# на вход принимает список
# возвращает объект DataFrame
def list_to_df(lst):
    df = pd.DataFrame(lst)
    return df


# функция для записи таблицы в csv-строку
# на вход принимает таблицу (DataFrame)
# возвращает csv-строку
def write_csv(df):
    csv_string = df.to_csv(header=False, index=False, encoding='utf-8')
    return csv_string
