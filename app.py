import csv
import json
import pandas as pd
import random as rng
import time

# алгоритм полного перебора
# алгоритм генерирует все возможные наборы признаков и для каждого набора проверяет его, попарно сравнивая сущности по признакам в наборе
# сложность алгоритма - O(2^m * n^2 * m), где
#   m - общее число признаков
#   n - общее число сущностей
def brute(objects):

  # получение списка возможных признаков сущностей
  properties = set()
  for object in objects:
    for property in object.keys():
      properties.add(property)
  properties.discard('about') # удаление признака about из примера, так как он однозначно определяет сущность
  properties = list(properties)

  # получение списка всех комбинаций признаков
  m = len(properties)
  subsets = list()
  for i in range(1, 1 << m):
    subsets.append(sorted([properties[j] for j in range(m) if (i & (1 << j))]))
  subsets.sort()
  
  # перебор всех комбинаций и выбор оптимальной (с наименьшим числом признаков)
  n = len(objects)
  optimal_subset = properties
  for subset in subsets:
    is_correct_subset = True

    # перебор всех пар сущностей
    for i in range(n):
      for j in range(i + 1, n):
        first_object = objects[i]
        second_object = objects[j]

        # проверка того, что очередная комбинация признаков различает данную пару сущностей
        is_different = False
        for property in subset:
          if not(property in first_object) and not(property in second_object):
            pass
          elif not(property in first_object) or not(property in second_object) or first_object[property] != second_object[property]:
            is_different = True

        # если комбинация не подходит, переход к следующей
        if not(is_different):
          is_correct_subset = False
          break
      if not(is_correct_subset):
        break
    
    # если комбинация подходит, ее длина сравнивается с длиной оптимальной комбинации, и если она меньше, то оптимальная комбинация обновляется
    if is_correct_subset and len(subset) < len(optimal_subset):
      optimal_subset = subset
  
  # перевод комбинации признаков в формат csv
  df = pd.DataFrame(optimal_subset)
  return df


# алгоритм перебора с отсечениями
# отличия от полного перебора:
#   список комбинаций признаков перемешивается
#   проверяются только комбинацци, длина которых меньше оптимальной
#   вместо попарного сравнения сущностей они поочередно добавляются в множество
# сложность алгоритма - O(2^m * n * m), где
#   m - общее число признаков
#   n - общее число сущностей
def optimized_brute(objects):

  # список возможных признаков сущностей и комбинаций признаков получаются аналогично полному перебору
  properties = set()
  for object in objects:
    for property in object.keys():
      properties.add(property)
  properties.discard('about')
  properties = list(properties)

  m = len(properties)
  subsets = list()
  for i in range(1, 1 << m):
    subsets.append(sorted([properties[j] for j in range(m) if (i & (1 << j))]))
  
  # перемешивание списка признаков
  rng.shuffle(subsets)

  # перебор комбинаций и выбор оптимальной (с наименьшим числом признаков)
  n = len(objects)
  optimal_subset = properties
  for subset in subsets:

    # если длина комбинации больше текущего оптимума, она пропускается
    if len(subset) >= len(optimal_subset):
      continue

    # создание множества для хранения и поиска значений призкаков сущностей
    set_objects = set()
    is_correct_subset = True
    for i in range(n):

      # получение списка значений признаков
      new_object = list()
      for property in subset:
        if property in objects[i]:
          new_object.append(objects[i][property])
      new_object = tuple(new_object)

      # если если сущность с такими значениями уже существует, то текущая комбинация не подходит
      if new_object in set_objects:
        is_correct_subset = False
        break

      # добавление значений признаков сущности в множество
      set_objects.add(new_object)
    
    # если комбинация подходит, ее длина сравнивается с длиной оптимальной комбинации, и если она меньше, то оптимальная комбинация обновляется
    if is_correct_subset and len(subset) < len(optimal_subset):
      optimal_subset = subset
  
  # перевод комбинации признаков в формат csv
  df = pd.DataFrame(optimal_subset)
  return df


# функция main
def main(input_string):
  objects = json.loads(input_string)
  df = optimized_brute(objects)
  df.to_csv('output.csv', header=False, index=False, encoding='utf-8')
  return open('output.csv', mode='r')


# функция для тестирования времени выполнения различных алгоритмов
def algorithm_test():
  data = json.load(open('input.json', 'r', encoding='utf-8'))
  input_string = json.dumps(data)
  objects = json.loads(input_string)
  time_start = time.time()
  df = brute(objects)
  df.to_csv('output_brute.csv', header=False, index=False, encoding='utf-8')
  time_br = time.time()
  df = optimized_brute(objects)
  df.to_csv('output_optimized.csv', header=False, index=False, encoding='utf-8')
  time_opt = time.time()

  print('полный перебор - ', round(time_br - time_start, 5), 'с', sep='')
  print('перебор с отсечениями - ', round(time_opt - time_br, 5), 'с', sep='')


def main_test():
  pass


algorithm_test()