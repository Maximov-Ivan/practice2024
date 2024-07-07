import time
from ..modules import load_json, write_scv
import brute
import optmized_brute


# функция для тестирования времени выполнения различных алгоритмов
def algorithm_test():
    objects = load_json('input.json')
    time_br_start = time.time()
    df = brute.brute(objects)
    time_br_end = time.time()
    time_br = round(time_br_end - time_br_start, 5)
    write_scv(df, 'output_br.csv')
    time_opt_start = time.time()
    df = optmized_brute.optimized_brute(objects)
    time_opt_end = time.time()
    time_opt = round(time_opt_end - time_opt_start, 5)
    write_scv(df, 'output_opt.csv')

    print('полный перебор - ', time_br, 'с', sep='')
    print('перебор с отсечениями - ', time_opt, 'с', sep='')
