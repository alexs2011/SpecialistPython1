# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы, то их ЗП уменьшается пропорционально,
# а за каждый час переработки они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"


d = {}

with open("workers.txt", "r", encoding="utf-8") as f:
    keys = f.readline().split()
    for line in f:
        tokens = line.split()
        d[(tokens[0], tokens[1])] = {}
        for i in range(len(keys)):
            d[(tokens[0], tokens[1])] |= {keys[i]: tokens[i]}

with open("hours_of.txt", "r", encoding="utf-8") as f:
    keys = f.readline().split()
    for line in f:
        tokens = line.split()
        k = tokens[0], tokens[1]
        d[k] = d[k] | {keys[2]: tokens[2]}

for key, val in d.items():
    goal = int(val['Норма_часов'])
    reality = int(val['Отработано'])
    salary = int(val['Зарплата'])
    money_per_hour = salary / goal
    if reality > goal:
        coef = (reality - goal) * money_per_hour * 2
        salary_real = goal * money_per_hour + coef
    else:
        salary_real = reality * money_per_hour
    d[key] = d[key] | {'Зарплата_фактическая': salary_real}

for val in d.values():
    print(f"{val['Имя']} {val['Фамилия']} {val['Зарплата_фактическая']:.2f}")
