# Дана строка из пяти целых чисел, разделенных пробелом.
# Пример входных данных: "2 12 -45 7 10"
# Напишите программу, которая находит среди них минимальное положительное число.
# Если таких чисел несколько - вывести любое из них.

# При решении задачи требуется учесть формат входных данных.
# Если входные данные некорректные, сообщить об этом.

while True:
    s = input("Введите 5 целых чисел через пробел: ")
    tokens = s.split()
    my_list = []
    try:
        if len(tokens) != 5:
            raise ValueError
        for i in range(5):
            my_list.append(int(tokens[i]))
        break
    except ValueError:
        print("Неверные входные данные")

my_list.sort()
min = my_list[4]
if min <= 0:
    print("Все числа меньше 0")
else:
    for el in my_list:
        if el < min and el > 0:
            min = el
print(min)
