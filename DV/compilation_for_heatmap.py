import csv
import os
import json

for filename in os.listdir('hashes_data'):
    output = []
    with open('hashes_data/' + filename, encoding='utf8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for line in reader:
            output.append({'time': line['time'], 'label': line['label'], 'lat': line['lat'], 'lng': line['lng'], 'value': 1})
    with open('heatmap_data/' + filename, mode='w', encoding='utf8', newline='') as f:
        fieldnames = ['time', 'label', 'lat', 'lng', 'value']
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(output)
