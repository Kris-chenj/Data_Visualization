import json
import csv
import os

def json_to_csv(input):
    with open(input,'r',encoding='utf8') as fp:
        json_data = json.load(fp)
    for tr in range(0,len(json_data)):
        divide = input.split("/")
        divide2 = divide[1].split('.')
        output = 'trajectories_csv/' + divide2[0]
        if not os.path.isdir(output):
            os.makedirs(output)
        outfile = output + '/' + str(tr) + '.csv' 
        with open(outfile,'w',encoding='utf8',newline="") as f:
            writer = csv.writer(f)   
            writer.writerow(["time","票据推销","色情欺诈","卡贷诱骗","商务广告"])
            for i in json_data[tr]["time"]:
                writer.writerow([i,int(json_data[tr]["time"][i][0]),int(json_data[tr]["time"][i][1]),int(json_data[tr]["time"][i][2]),int(json_data[tr]["time"][i][3])])

input_basis = "trajectories/201702"
for i in range(23,29):
    input_file = input_basis + str(i) + ".json"
    json_to_csv(input_file)

input_basis = "trajectories/2017030"
for i in range(1,10):
    input_file = input_basis + str(i) + ".json"
    json_to_csv(input_file)

input_basis = "trajectories/201703"
for i in range(10,32):
    input_file = input_basis + str(i) + ".json"
    json_to_csv(input_file)

input_basis = "trajectories/2017040"
for i in range(1,10):
    input_file = input_basis + str(i) + ".json"
    json_to_csv(input_file)

input_basis = "trajectories/201704"
for i in range(10,27):
    input_file = input_basis + str(i) + ".json"
    json_to_csv(input_file)