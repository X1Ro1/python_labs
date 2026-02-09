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

    f = open(filename, "r")

    read = csv.reader(f)
    next(read)
    for row in read:
        category = row[0]
        val = float(row[1])
        data[category].append(val)

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

MedianAll = {
    "A": [],
    "B": [],
    "C": [],
    "D": []
}

for file in files:
    res = process_file(file)

    for cat in res:
        MedianAll[cat].append(res[cat][0])


print("\nИтоговый результат:")
print("Категория  Медиана медиан  Стандартное отклонение")

for cat in MedianAll:
    medMeds = statistics.median(MedianAll[cat])

    if len(MedianAll[cat]) > 1:
        stdMeds = statistics.stdev(MedianAll[cat])
    else:
        stdMeds = 0

    print(cat, " " * 8, round(medMeds, 2), " " * 10, round(stdMeds, 2))
