import json
import pandas as pd


# функция для чтения формата json
# на вход принимает файл json
# возвращает объект Python (обычно список или словарь,
# в зависимости от структуры входного файла)
def load_json(filename):
    objects = json.load(open(filename, 'r', encoding='utf-8'))
    return objects


# функция для получения списка возможных признаков сущностей
# на вход принимает набор сущностей
# возвращает список возможных признаков
def get_properties(objects):
    properties = set()
    for object in objects:
        for property in object.keys():
            properties.add(property)
    properties = list(properties)
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
def list_to_df(list):
    df = pd.DataFrame(list)
    return df


# функция для записи таблицы в файл формата csv
# на вход принимает таблицу (DataFrame) и имя файла
# возвращает файл формата csv
def write_scv(df, filename='output.csv'):
    df.to_csv(filename, header=False, index=False, encoding='utf-8')
    return open(filename, mode='r')
