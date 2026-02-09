import csv
import random
import statistics

for i in range(5):
    f = open("data" + str(i+1) + ".csv", "w")
    wr = csv.writer(f)

    wr.writerow(["Категория", "Значение"])

    for j in range(1000):
        c = random.choice(["A", "B", "C", "D"])
        v = random.random() * 100
        wr.writerow([c, v])

    f.close()
print("Файлы созданы")


def process_file(filename):
    data = {
        "A": [],
        "B": [],
        "C": [],
        "D": []
    }

    f = open(filename, "r", encoding="utf-8")

    read = csv.reader(f)
    next(read)
    for row in read:
        category = row[0]
        value = float(row[1])
        data[category].append(value)

    res = {}
    for cat in data:
        if len(data[cat]) > 0:
            med = statistics.median(data[cat])
            if len(data[cat]) > 1:
                std = statistics.stdev(data[cat])
            else:
                std = 0
        else:
            med = 0
            std = 0
        res[cat] = (round(med, 2), round(std, 2))

    return res


files = ["data_1.csv", "data_2.csv", "data_3.csv", "data_4.csv", "data_5.csv"]

all_medians = {
    "A": [],
    "B": [],
    "C": [],
    "D": []
}

for file in files:
    res = process_file(file)

    for cat in res:
        all_medians[cat].append(res[cat][0])


print("\nИтоговый результат:")
print("Категория  Медиана медиан  Стандартное отклонение")

for cat in all_medians:
    med_of_meds = statistics.median(all_medians[cat])

    if len(all_medians[cat]) > 1:
        std_of_meds = statistics.stdev(all_medians[cat])
    else:
        std_of_meds = 0

    print(cat, " " * 8, round(med_of_meds, 2), " " * 10, round(std_of_meds, 2))
