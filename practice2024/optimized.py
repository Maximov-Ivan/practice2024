from .modules import load_json, get_properties, get_subsets, group_by_len, list_to_df, write_csv


# алгоритм перебора с отсечениями
# отличия от полного перебора:
#     вместо попарного сравнения сущностей они добавляются в множество
#     комбинации группируются по длине и проверяются от больших к меньшим
# сложность алгоритма - O(2^m * n * m / C), где
#     m - общее число признаков
#     n - общее число сущностей
#     C - некоторая константа отсечений
# на вход принимает набор сущностей
# возвращает минимальный по составу набор признаков, позволяющий
# однозначно идентифицировать сущность в наборе
def optimized(json_string):

    # чтение формата json
    objects = load_json(json_string)

    # получение списка возможных признаков сущностей
    properties, m = get_properties(objects)

    # получение списка всех комбинаций признаков
    subsets = get_subsets(properties)

    # группировака списка комбинаций признаков по длине
    grouped_subsets = group_by_len(subsets, m)

    # перебор комбинаций в порядке уменьшения длины
    # и выбор оптимальной (с наименьшим числом признаков)
    n = len(objects)
    optimal_subset = properties
    subset_len = m - 1
    while subset_len > 0:
        updated_optimal = False
        for subset in grouped_subsets[subset_len]:

            # создание множества для хранения
            # и поиска значений призкаковсущностей
            set_objects = set()
            is_correct_subset = True
            for i in range(n):

                # получение списка значений признаков
                new_object = list()
                for property in subset:
                    if property in objects[i]:
                        new_object.append(objects[i][property])
                new_object = tuple(new_object)

                # если если сущность с такими значениями уже существует,
                # то текущая комбинация не подходит
                if new_object in set_objects:
                    is_correct_subset = False
                    break

                # добавление значений признаков сущности в множество
                set_objects.add(new_object)

            # если комбинация подходит, то оптимальная комбинация обновляется
            # и делается переход к меньшей длине комбинации
            if is_correct_subset:
                optimal_subset = subset
                updated_optimal = True
                subset_len -= 1
                break

        # если не удалось обновить оптимум всеми комбинациями некоторой длины,
        # завершае цикл (обновить комбинациями меньшей длины тоже не получится)
        if not (updated_optimal):
            break

    # перевод комбинации признаков в DataFrame
    df = list_to_df(optimal_subset)

    # запись таблицы в csv-строку
    csv_string = write_csv(df)

    return csv_string
