from .optimized import optimized


# функция main
# на вход принимает json-строку с исходными данными
# возвращает таблицу одной колонкой - искомый набор имен признаков
# в виде csv-строки
def main(input):
    output = optimized(input)
    return output
