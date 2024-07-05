import csv
import json
import pandas as pd

# алгоритм полного перебора
# сложность алгоритма - O(2^m * n^2 * m), где
#   m - общее число признаков
#   n - общее число сущностей
def brute(objects):

  # получение списка возможных признаков сущностей
  properties = set()
  for object in objects:
    for property in object.keys():
      properties.add(property)
  properties.discard('about') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
  df.to_csv('output.csv', header=False, index=False)


def main(input_string):
  objects = json.loads(input_string)
  brute(objects)
  

data = json.load(open('input.json', 'r', encoding='utf-8'))
input_string = json.dumps(data)
main(input_string)