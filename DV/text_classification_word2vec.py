import jieba
import csv
import re
from sklearn.cluster import KMeans
import numpy as np
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def process_each_file(inputfile,outputfile,kmeans2,seg_dict,stop_words,output_jpg):
    with open(inputfile, mode='r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        all_content = []
        content = []
        count = 0
        sentence_frequency = []    
        for line in reader:
            stri = simplify(line['content'])
            if len(stri) <= 8:
                continue
            all_content.append(line)
            all_content[count]['label'] = -1
            content.append({'bow': [], 'label': 0, 'seg': [], 'text': stri})
            words = jieba.lcut(stri)
            filtered_words = []
            for j in words:
                if j not in stop_words:
                    filtered_words.append(j)
            content[count]['seg'] = filtered_words
            content[count]['bow'] = [0 for i in range(8)]
            for seg in content[count]['seg']:
                content[count]['bow'][seg_dict[seg]] += 1
            sentence_frequency.append(content[count]['bow'])
            count += 1
    
    sentence_label = kmeans2.predict(sentence_frequency)
    for i in range(len(sentence_label)):
        all_content[i]['label'] = sentence_label[i]
        all_content[i]['sentence_frequency'] = sentence_frequency[i]

    with open(outputfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["md5","content","phone","conntime","recitime","lng","lat","label","sentence_frequency"])   
        writer.writeheader()
        writer.writerows(all_content)
    
    # 
    # visualization(sentence_frequency,sentence_label,output_jpg)

def visualization(sentence_frequency,sentence_label,output_jpg):
    data = PCA(n_components=2).fit_transform(np.array(sentence_frequency))
    x = [item[0] for item in data]
    y = [item[1] for item in data]

    color_mapping = ['b', 'g', 'r', 'c']
    color = [color_mapping[item] for item in sentence_label]

    plt.scatter(x, y, c=color)
    # for i in range(len(labels)):
    #      plt.annotate(seg_list[i], xy = (x[i], y[i]))
    plt.savefig(output_jpg)

def simplify(text):
    output = re.sub('\W', '', re.sub('[a-zA-Z0-9]', '', text))
    return output


def vectorize(cut_word_list, model):
    features = []
    for tokens in cut_word_list:
        zero_vector = np.zeros(model.vector_size)
        vectors = []
        for token in tokens:
            if token in model.wv:
                try:
                    vectors.append(model.wv[token])
                except KeyError:
                    continue
        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            features.append(avg_vec)
        else:
            features.append(zero_vector)
    return features


# mpl.rcParams['font.sans-serif'] = ['SimHei']

#### Get the model ####
content = []
count = 0
with open('output.csv', mode='r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    print('reading lines')
    for line in reader:
        stri = simplify(line['content'])
        if len(stri) <= 8:
            continue
        content.append({'bow': [], 'label': 0, 'seg': [], 'text': stri})
        count += 1
        if count % 1000 == 0:
            print(count, '/', 180000)


stop_words = ['的', '了', '你', '你好', '您好', '您', '我', '可', '本', '各', '后', '将', '在', '完成', '有', '已', '吗', '如', '在']

seg_dict = {}
count = 0
cut_word_list = []
print('cutting words')
# construct empty seg dict
for i in range(len(content)):
    count += 1
    if count % 1000 == 0:
        print(count, '/', 180000)
    words = jieba.lcut(content[i]['text'])
    filtered_words = []
    for j in words:
        if j not in stop_words:
            filtered_words.append(j)
    content[i]['seg'] = filtered_words
    cut_word_list.append(content[i]['seg'])
    for seg in content[i]['seg']:
        try:
            seg_dict[seg] += 0
        except:
            seg_dict[seg] = 0

model = Word2Vec(sentences=cut_word_list)

vector_word = []
word_in_model = []
for key in seg_dict:
    try:
        vector_word.append(model.wv[key])
    except:
        vector_word.append(np.zeros(100))

init_vector = []
kmeans1 = KMeans(n_clusters=8).fit(vector_word)
labels = kmeans1.predict(vector_word)
i = 0
for key in seg_dict:
    seg_dict[key] = labels[i]
    i += 1

sentence_frequency = []
for i in range(0, len(content)):
    content[i]['bow'] = [0 for i in range(8)]
    # length = len(content[i][1])
    for seg in content[i]['seg']:
        content[i]['bow'][seg_dict[seg]] += 1
    sentence_frequency.append(content[i]['bow'])

kmeans2 = KMeans(n_clusters=4, random_state=4).fit(sentence_frequency)
sentence_label = kmeans2.predict(sentence_frequency)
for i in range(len(sentence_label)):
    content[i]['label'] = sentence_label[i]

centers = kmeans2.cluster_centers_
print(centers)

with open("text_classification.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["bow","label","seg","text"])   
    writer.writeheader() # 写入列名
    writer.writerows(content) # 写入数据
print('model done')
output_jpg = "./classification_overall/overall.jpg"
visualization(sentence_frequency,sentence_label,output_jpg)

# sentence_frequency0 = []
# sentence_frequency1 = []
# sentence_frequency2 = []
# sentence_frequency3 = []
# index0 = []
# index1 = []
# index2 = []
# index3 = []
# for i in range(len(sentence_label)):
#     if sentence_label[i] == 0:
#         sentence_frequency0.append(sentence_frequency[i])
#         index0.append(i)
#     if sentence_label[i] == 1:
#         sentence_frequency1.append(sentence_frequency[i])
#         index1.append(i)
#     if sentence_label[i] == 2:
#         sentence_frequency2.append(sentence_frequency[i])
#         index2.append(i)
#     if sentence_label[i] == 3:
#         sentence_frequency3.append(sentence_frequency[i])
#         index3.append(i)

# sentence_label0 = KMeans(n_clusters=4, random_state=4).fit_predict(sentence_frequency0)
# with open("classification0.csv","w",encoding="utf-8",newline="") as f:
#     writer = csv.writer(f)
#     for i in range(len(sentence_label0)):
#         writer.writerow([sentence_label0[i],"".join(content[index0[i]]['text'])])
# sentence_label1 = KMeans(n_clusters=2, random_state=2).fit_predict(sentence_frequency1)
# with open("classification1.csv","w",encoding="utf-8",newline="") as f:
#     writer = csv.writer(f)
#     for i in range(len(sentence_label1)):
#         writer.writerow([sentence_label1[i],"".join(content[index1[i]]['text'])])
# sentence_label3 = KMeans(n_clusters=2, random_state=2).fit_predict(sentence_frequency3)
# with open("classification3.csv","w",encoding="utf-8",newline="") as f:
#     writer = csv.writer(f)
#     for i in range(len(sentence_label3)):
#         writer.writerow([sentence_label3[i],"".join(content[index3[i]]['text'])])
# output_jpg = "./classification_1/overall.jpg"
# visualization(sentence_frequency0,sentence_label0,output_jpg)
#### Use the model ####
input_basis = "./data/201702"
output_basis = "./processed_data/201702"
output_jpg_basis = "./classification_overall/201702"
for i in range(23,29):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    output_jpg = output_jpg_basis + str(i) + ".jpg"
    process_each_file(input_file,output_file,kmeans2,seg_dict,stop_words,output_jpg)

input_basis = "./data/2017030"
output_basis = "./processed_data/2017030"
output_jpg_basis = "./classification_overall/2017030"
for i in range(1,10):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    output_jpg = output_jpg_basis + str(i) + ".jpg"
    process_each_file(input_file,output_file,kmeans2,seg_dict,stop_words,output_jpg)

input_basis = "./data/201703"
output_basis = "./processed_data/201703"
output_jpg_basis = "./classification_overall/201703"
for i in range(10,32):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    output_jpg = output_jpg_basis + str(i) + ".jpg"
    process_each_file(input_file,output_file,kmeans2,seg_dict,stop_words,output_jpg)

input_basis = "./data/2017040"
output_basis = "./processed_data/2017040"
output_jpg_basis = "./classification_overall/2017040"
for i in range(1,10):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    output_jpg = output_jpg_basis + str(i) + ".jpg"
    process_each_file(input_file,output_file,kmeans2,seg_dict,stop_words,output_jpg)

input_basis = "./data/201704"
output_basis = "./processed_data/201704"
output_jpg_basis = "./classification_overall/201704"
for i in range(10,27):
    input_file = input_basis + str(i) + ".csv"
    output_file = output_basis + str(i) + ".csv"
    output_jpg = output_jpg_basis + str(i) + ".jpg"
    process_each_file(input_file,output_file,kmeans2,seg_dict,stop_words,output_jpg)
