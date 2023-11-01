import warnings
warnings.filterwarnings("ignore")
import jieba   
import csv
from wordcloud import WordCloud
import re

def simplify(text):
    output = re.sub('\W', '', re.sub('[a-zA-Z0-9]', '', text))
    return output

def createSuperWordCloud(text_path,output):
    text = []
    with open(text_path,'r',encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stri = simplify(row['content'])
            if len(stri) <= 8:
                continue
            text.append({"text":stri,"label":row['label']})
        
    stop_words = ['于','的', '了', '你', '你好', '您好', '您', '我', '可', '本', '各', '后', '将', '在', '完成', '有', '已', '吗', '如', '在','请','打','开','二','日','点','一个','等','今日','根据']

    segment = {}
    label_list = []
    for l in text:
        line = str(l['text'])
        segs=jieba.lcut(line)
        for seg in segs:
            if seg not in stop_words:
                try:
                    segment[seg] += 1
                except:
                    segment[seg] = 1
                    label_list.append(l['label'])

    
    integrity = [] 
    index = 0
    for seg in segment:
        integrity.append([seg,segment[seg],label_list[index]])
        index += 1
    sorted_segment = sorted(integrity,key=lambda x:x[1],reverse=True)
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)   
        writer.writerow(['word','frequency','label'])
        for i in range(0,200):
            writer.writerow([sorted_segment[i][0],sorted_segment[i][1],sorted_segment[i][2]])
        

input_basis = "./processed_data/201702"
output_basis = "./word_cloud/201702"
for i in range(23,29):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    createSuperWordCloud(input_file,output_file)

input_basis = "./processed_data/2017030"
output_basis = "./word_cloud/2017030"
for i in range(1,10):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    createSuperWordCloud(input_file,output_file)

input_basis = "./processed_data/201703"
output_basis = "./word_cloud/201703"
for i in range(10,32):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    createSuperWordCloud(input_file,output_file)

input_basis = "./processed_data/2017040"
output_basis = "./word_cloud/2017040"
for i in range(1,10):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    createSuperWordCloud(input_file,output_file)

input_basis = "./processed_data/201704"
output_basis = "./word_cloud/201704"
for i in range(10,27):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    createSuperWordCloud(input_file,output_file)
