import csv
import time
import pandas as pd

for k in range(1,10):

    fil = "time.slot" + "_4-0" + str(k) + ".csv"
    with open(fil,"a+",newline='') as wri:
        writ = csv.writer(wri)
        writ.writerow(["4-0" + str(k)])

    ans = []
    for i in range(0,24):
        hour = []
        for j in range(0,12):
            slot = [0,0,0,0]
            hour.append(slot)
        ans.append(hour)

    source = "processed_data/2017040" + str(k) + ".csv"
    data = pd.read_csv(source)
    for i in range(0,len(data["recitime"])):
        label = int(data["label"][i])
        timeArray = time.localtime(int(data["recitime"][i] / 1000))
        tim = time.strftime('%Y-%m-%d %H:%M:%S',timeArray)
        sli = tim.split()[1].split(":")
        x = int(sli[0])
        y = int(int(sli[1]) / 5)
        ans[x][y][label] += 1

    with open(fil,"a+",newline='') as wri:
        writ = csv.writer(wri)
        for i in range(0,24):
            writ.writerows(ans[i])


for k in range(10,32):

    fil = "time.slot" + "_4-" + str(k) + ".csv"
    with open(fil,"a+",newline='') as wri:
        writ = csv.writer(wri)
        writ.writerow(["4-" + str(k)])

    ans = []
    for i in range(0,24):
        hour = []
        for j in range(0,12):
            slot = [0,0,0,0]
            hour.append(slot)
        ans.append(hour)

    source = "processed_data/201704" + str(k) + ".csv"
    data = pd.read_csv(source)
    for i in range(0,len(data["recitime"])):
        label = int(data["label"][i])
        timeArray = time.localtime(int(data["recitime"][i] / 1000))
        tim = time.strftime('%Y-%m-%d %H:%M:%S',timeArray)
        sli = tim.split()[1].split(":")
        x = int(sli[0])
        y = int(int(sli[1]) / 5)
        ans[x][y][label] += 1

    with open(fil,"a+",newline='') as wri:
        writ = csv.writer(wri)
        for i in range(0,24):
            writ.writerows(ans[i])