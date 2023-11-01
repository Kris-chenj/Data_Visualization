import csv
import pandas as pd

with open("time_line.csv","w") as wri:
        writ = csv.writer(wri)
        writ.writerow(["Date","票据推销","色情欺诈","卡贷诱骗","商务广告"])

j = 2.23
for i in range(23,29):
    path = "processed_data/201702" + str(i) + ".csv"
    data = pd.read_csv(path)
    lentt = len(data["label"])
    ans = [str(format(j,'.2f')),0,0,0,0]
    for i in range(0,lentt):
        if(data["label"][i] == 0):
            ans[1] += 1
        if(data["label"][i] == 1):
            ans[2] += 1
        if(data["label"][i] == 2):
            ans[3] += 1
        if(data["label"][i] == 3):
            ans[4] += 1
    with open("time_line.csv","a+") as wri:
        writ = csv.writer(wri)
        writ.writerow(ans)
    j += 0.01

j = 3.01
for i in range(1,10):
    path = "processed_data/2017030" + str(i) + ".csv"
    data = pd.read_csv(path)
    lentt = len(data["label"])
    ans = [str(format(j,'.2f')),0,0,0,0]
    for i in range(0,lentt):
        if(data["label"][i] == 0):
            ans[1] += 1
        if(data["label"][i] == 1):
            ans[2] += 1
        if(data["label"][i] == 2):
            ans[3] += 1
        if(data["label"][i] == 3):
            ans[4] += 1
    with open("time_line.csv","a+") as wri:
        writ = csv.writer(wri)
        writ.writerow(ans)
    j += 0.01

j = 3.10
for i in range(10,32):
    path = "processed_data/201703" + str(i) + ".csv"
    data = pd.read_csv(path)
    lentt = len(data["label"])
    ans = [str(format(j,'.2f')),0,0,0,0]
    for i in range(0,lentt):
        if(data["label"][i] == 0):
            ans[1] += 1
        if(data["label"][i] == 1):
            ans[2] += 1
        if(data["label"][i] == 2):
            ans[3] += 1
        if(data["label"][i] == 3):
            ans[4] += 1
    with open("time_line.csv","a+") as wri:
        writ = csv.writer(wri)
        writ.writerow(ans)
    j += 0.01

j = 4.01
for i in range(1,10):
    path = "processed_data/2017040" + str(i) + ".csv"
    data = pd.read_csv(path)
    lentt = len(data["label"])
    ans = [str(format(j,'.2f')),0,0,0,0]
    for i in range(0,lentt):
        if(data["label"][i] == 0):
            ans[1] += 1
        if(data["label"][i] == 1):
            ans[2] += 1
        if(data["label"][i] == 2):
            ans[3] += 1
        if(data["label"][i] == 3):
            ans[4] += 1
    with open("time_line.csv","a+") as wri:
        writ = csv.writer(wri)
        writ.writerow(ans)
    j += 0.01

j = 4.10
for i in range(10,27):
    path = "processed_data/201704" + str(i) + ".csv"
    data = pd.read_csv(path)
    lentt = len(data["label"])
    ans = [str(format(j,'.2f')),0,0,0,0]
    for i in range(0,lentt):
        if(data["label"][i] == 0):
            ans[1] += 1
        if(data["label"][i] == 1):
            ans[2] += 1
        if(data["label"][i] == 2):
            ans[3] += 1
        if(data["label"][i] == 3):
            ans[4] += 1
    with open("time_line.csv","a+") as wri:
        writ = csv.writer(wri)
        writ.writerow(ans)
    j += 0.01