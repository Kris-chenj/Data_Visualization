import csv

output = []
last_text = ''
with open('output.csv', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        text = line['content']
        if text != last_text:
            last_text = text
            text = text.replace('\n', '')
            output.append(text)

with open('text.csv', mode='w', encoding='utf8') as f:
    for line in output:
        f.write(line + '\n')