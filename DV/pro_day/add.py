

# for i in range(1,10):
#     ans = []
#     path = "time_slot_data/time.slot_4-0" + str(i) + ".csv"
    
#     with open(dest,"a+",newline='') as wri:
#         writ = csv.writer(wri)
#         writ.writerows(ans)
    
# for i in range(10,27):
#     ans = []
#     path = "time_slot_data/time.slot_4-" + str(i) + ".csv"
    
#     with open(dest,"a+",newline='') as wri:
#         writ = csv.writer(wri)
#         writ.writerows(ans)

for i in range(1,10):
    path = "pro_4-0" + str(i) + ".csv"
    with open(path, "r+") as f:
        old = f.read()
        f.seek(0)
        f.write("key,value,date\n")
        f.write(old)

for i in range(10,27):
    path = "pro_4-" + str(i) + ".csv"
    with open(path, "r+") as f:
        old = f.read()
        f.seek(0)
        f.write("key,value,date\n")
        f.write(old)