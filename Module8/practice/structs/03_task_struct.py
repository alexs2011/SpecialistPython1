# Дан список, заполненный произвольными целыми числами.
# Примечание: для генерации списка используйте функцию.
# Найдите:
# 1. Количество элементов списка не превышающие 10
# 2. Сумму всех положительных элементов списка
# 3. Среднее арифметическое всех четных элементов
import random


def rand_list(n):
    res = []
    for _ in range(n):
        res.append(random.randint(-20, 20))
    return res


lst = rand_list(10)
print(lst)
count = len(list(filter(lambda x: x <= 10, lst)))
print(count)
s = sum(filter(lambda x: x > 0, lst))
print(s)
n = list(filter(lambda x: x % 2 == 0 and x > 0, lst))
avg = sum(n) / len(n)
print(avg)
