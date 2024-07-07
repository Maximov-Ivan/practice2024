import modules
import optmized_brute


# функция main
def main(input):
    objects = modules.load_json(input)
    answer = optmized_brute.optimized_brute(objects)
    return modules.write_csv(answer)
