# Дан файл ("data/fruits.txt") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А.txt, fruits_Б.txt, fruits_В.txt ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов и
# распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))


# Результаты для файла в 10_000_000 строк (на hdd):
# Версия 1: Общее время: 9.56, открытие файла: 5.98, запись: 3.58
# Версия 2: Общее время: 6.62, открытие файла: 5.74, запись: 0.88
# Версия 3: Общее время: 4.51, открытие файла: 4.30, запись: 0.20
# Версия 4: Общее время: 3.08, открытие файла: 2.86, запись: 0.22
# Версия 5: Общее время: 2.83, открытие файла: 2.58, запись: 0.25


import time
import mmap

in_file = "fruits.txt"
out_file = "data/fruits"

# Версия 1

d = {}

t1 = time.time()

f = open(f"{in_file}", "r", encoding="utf-8")

for word in f:
    if word.strip() == "":
        continue

    if d.get(word[0]) is None:
        d[word[0]] = []
    val = d[word[0]]
    val.append(word.rstrip())
    d[word[0]] = val

f.close()

t2 = time.time()

for key, val in d.items():
    f = open(f"{out_file}_{key}.txt", "w", encoding="utf-8")
    for fruit in val:
        f.write(fruit + "\n")
    f.close()

t3 = time.time()

print(f"Общее время: {t3 - t1:.2f}, открытие файла: {t2 - t1:.2f}, запись: {t3 - t2:.2f}")

# Версия 2

d = {}

t1 = time.time()

with open(f"{in_file}", "r", encoding="utf-8") as f:
    for word in f:
        if word == "\n":
            continue
        d.setdefault(word[0], bytearray()).extend(bytearray(word, "utf-8"))

t2 = time.time()

for key, val in d.items():
    with open(f"{out_file}_{key}.txt", "w", encoding="utf-8") as f:
        f.write(val.decode())

t3 = time.time()

print(f"Общее время: {t3 - t1:.2f}, открытие файла: {t2 - t1:.2f}, запись: {t3 - t2:.2f}")

# Версия 3

d = {}

t1 = time.time()

with open(f"{in_file}", "r", encoding="utf-8") as file_obj:
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
        line = mmap_obj.readline()
        blank_str = bytearray("\r\n", "utf-8")
        while line:
            if line == blank_str:
                line = mmap_obj.readline()
                continue
            d.setdefault(line[0:2], bytearray()).extend(line)
            line = mmap_obj.readline()

t2 = time.time()

for key, val in d.items():
    with open(f"{out_file}_{key.decode()}.txt", "wb") as file_obj:
        file_obj.seek(len(val) - 1)
        file_obj.write(b"\0")
    with open(f"{out_file}_{key.decode()}.txt", mode="r+b") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            mmap_obj.write(val)

t3 = time.time()

print(f"Общее время: {t3 - t1:.2f}, открытие файла: {t2 - t1:.2f}, запись: {t3 - t2:.2f}")


# Версия 4

def create_dict(i):
    i += end_of_line
    d.setdefault(i[0:2], bytearray()).extend(i)


d = {}

t1 = time.time()

end_of_line = b"\n"

with open(f"{in_file}", "r", encoding="utf-8") as file_obj:
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
        file_cont = mmap_obj.read().split(bytearray("\r\n\r\n", "utf-8"))
        tuple(map(create_dict, file_cont))

t2 = time.time()

for key, val in d.items():
    with open(f"{out_file}_{key.decode()}.txt", "wb") as file_obj:
        file_obj.seek(len(val) - 1)
        file_obj.write(b"\0")
    with open(f"{out_file}_{key.decode()}.txt", mode="r+b") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            mmap_obj.write(val)

t3 = time.time()

print(f"Общее время: {t3 - t1:.2f}, открытие файла: {t2 - t1:.2f}, запись: {t3 - t2:.2f}")


# Версия 5 (на 0.15-0.2 секунды быстрее 4-й версии)

def create_dict_2(i):
    d.setdefault(i[1:3], bytearray()).extend(i)


d = {}

t1 = time.time()

with open(f"{in_file}", "r", encoding="utf-8") as file_obj:
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
        file_cont = mmap_obj.read().split(bytearray("\r\n\r", "utf-8"))
        tuple(map(create_dict_2, file_cont))

t2 = time.time()

# Вставляем на место самую первую строку, которая попала не туда
key_orig = next(iter(d))
val = d[bytes(key_orig)]
d.pop(bytes(key_orig), None)
key = val[0:2]
new_val = d[bytes(key)]
val = b"\n" + val
val += new_val
d[bytes(key)] = val

for key, val in d.items():
    with open(f"{out_file}_{key.decode()}.txt", "wb") as file_obj:
        file_obj.seek(len(val) - 2)
        file_obj.write(b"\0")
    with open(f"{out_file}_{key.decode()}.txt", mode="r+b") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            mmap_obj.write(val[1:])

t3 = time.time()

print(f"Общее время: {t3 - t1:.2f}, открытие файла: {t2 - t1:.2f}, запись: {t3 - t2:.2f}")
