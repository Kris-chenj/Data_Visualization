import csv
import time
from datetime import datetime, timedelta
import pandas as pd

def generate_time_series(start, end):
    current = datetime.strptime(start, '%H/%M')
    end_item = datetime.strptime(end, '%H/%M')
    time_delta = timedelta(minutes=5)
    time_series = ["00/03"]
    while current < end_item:
        next = current + time_delta
        ele = str(next.hour)
        if(next.hour < 10):
            if(next.minute < 10):
                ele = "0" + ele + "/" + "0" + str(next.minute)
            else:
                ele = "0" + ele + "/" + str(next.minute)
        else:
            if(next.minute < 10):
                ele = ele + "/" + "0" + str(next.minute)
            else:
                ele = ele + "/" + str(next.minute)
        time_series.append(ele)
        current = next
    return time_series


if __name__=="__main__":
    timeslot = generate_time_series("00/03","23/58")

    for i in range(23,29):
        ans = []
        e = []
        e.append("key")
        e.append("value")
        e.append("date")
        ans.append(e)
        path = "time_slot_data/time.slot_2-" + str(i) + ".csv"
        
        data = pd.read_csv(path, names=["0", "1", "2", "3"], header=0)
        lent = len(data["0"])
        for j in range(0,4):
            for k in range(0,lent):
                ele = []
                if(j == 0):
                    ele.append("票据推销")
                elif(j == 1):
                    ele.append("色情欺诈")
                elif(j == 2):
                    ele.append("卡贷诱骗")
                elif(j == 3):
                    ele.append("商务广告")
                
                ele.append(data[str(j)][k])
                ele.append(timeslot[k])
                ans.append(ele)
        
        dest = "pro_2-" + str(i) + ".csv"
        with open(dest,"a+",newline='',encoding='utf-8') as wri:
            writ = csv.writer(wri)
            writ.writerows(ans)
            
    # for i in range(1,10):
    #     ans = []
    #     e = []
    #     e.append("key")
    #     e.append("value")
    #     e.append("date")
    #     ans.append(e)
    #     path = "time_slot_data/time.slot_3-0" + str(i) + ".csv"
        
    #     data = pd.read_csv(path, names=["0", "1", "2", "3"], header=0)
    #     lent = len(data["0"])
    #     for j in range(0,4):
    #         for k in range(0,lent):
    #             ele = []
    #             if(j == 0):
    #                 ele.append("票据推销")
    #             elif(j == 1):
    #                 ele.append("色情欺诈")
    #             elif(j == 2):
    #                 ele.append("卡贷诱骗")
    #             elif(j == 3):
    #                 ele.append("商务广告")
                
    #             ele.append(data[str(j)][k])
    #             ele.append(timeslot[k])
    #             ans.append(ele)
        
    #     dest = "pro_3-0" + str(i) + ".csv"
    #     with open(dest,"a+",newline='',encoding='utf-8') as wri:
    #         writ = csv.writer(wri)
    #         writ.writerows(ans)
    
    # for i in range(10,32):
    #     ans = []
    #     e = []
    #     e.append("key")
    #     e.append("value")
    #     e.append("date")
    #     ans.append(e)
    #     path = "time_slot_data/time.slot_3-" + str(i) + ".csv"
        
    #     data = pd.read_csv(path, names=["0", "1", "2", "3"], header=0)
    #     lent = len(data["0"])
    #     for j in range(0,4):
    #         for k in range(0,lent):
    #             ele = []
    #             if(j == 0):
    #                 ele.append("票据推销")
    #             elif(j == 1):
    #                 ele.append("色情欺诈")
    #             elif(j == 2):
    #                 ele.append("卡贷诱骗")
    #             elif(j == 3):
    #                 ele.append("商务广告")
                
    #             ele.append(data[str(j)][k])
    #             ele.append(timeslot[k])
    #             ans.append(ele)
        
    #     dest = "pro_3-" + str(i) + ".csv"
    #     with open(dest,"a+",newline='',encoding='utf-8') as wri:
    #         writ = csv.writer(wri)
    #         writ.writerows(ans)
