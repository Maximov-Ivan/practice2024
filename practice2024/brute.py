from .modules import load_json, get_properties, get_subsets, list_to_df, write_csv


# алгоритм полного перебора
# алгоритм генерирует все возможные наборы признаков и для каждого набора
# проверяет его, попарно сравнивая сущности по признакам в наборе
# сложность алгоритма - O(2^m * n^2 * m), где
#     m - общее число признаков
#     n - общее число сущностей
# на вход принимает набор сущностей
# возвращает минимальный по составу набор признаков, позволяющий
# однозначно идентифицировать сущность в наборе
def brute(json_string):

    # чтение формата json
    objects = load_json(json_string)

    # получение списка возможных признаков сущностей
    properties, m = get_properties(objects)

    # получение списка всех комбинаций признаков
    subsets = get_subsets(properties)

    # перебор всех комбинаций и выбор оптимальной
    # (с наименьшим числом признаков)
    n = len(objects)
    optimal_subset = properties
    for subset in subsets:
        is_correct_subset = True

        # перебор всех пар сущностей
        for i in range(n):
            for j in range(i + 1, n):
                first_obj = objects[i]
                second_obj = objects[j]

                # проверка того, что очередная комбинация признаков
                # различает данную пару сущностей
                is_different = check_subset(subset, first_obj, second_obj)

                # если комбинация не подходит, переход к следующей
                if not (is_different):
                    is_correct_subset = False
                    break
            if not (is_correct_subset):
                break

        # если комбинация подходит, ее длина сравнивается с длиной оптимальной
        # комбинации, и если она меньше, то оптимальная комбинация обновляется
        if is_correct_subset and len(subset) < len(optimal_subset):
            optimal_subset = subset

    # перевод комбинации признаков в DataFrame
    df = list_to_df(optimal_subset)

    # запись таблицы в csv-строку
    csv_string = write_csv(df)

    return csv_string


# проверка того, что очередная комбинация признаков
# различает данную пару сущностей
def check_subset(subset, first_obj, second_obj):
    is_different = False
    for property in subset:
        if not (property in first_obj) \
           and not (property in second_obj):
            pass
        if not (property in first_obj) \
           or not (property in second_obj) \
           or first_obj[property] != second_obj[property]:
            is_different = True
    return is_different
