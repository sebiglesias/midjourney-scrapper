import requests
import json
import urllib.request
import csv
from PIL import Image, ImageOps
from datetime import datetime
from instagrapi import Client
import sys

client = sys.argv[1]
secret = sys.argv[2]

url = sys.argv[3]

# Perform Request
print('# Perform Request')
response = requests.get(url)
print(response.status_code)

# Get Response
print('# Get Response')
jsonRes = json.loads(response.text)

# Download Images
print('# Download Images')
dict = {}
dt = datetime.now().weekday().real
for index, item in enumerate(range(dt * 4, (dt * 4) + 3)):
    elem = jsonRes[item]
    dict['{}.jpg'.format(index)] = elem['prompt']
    print(index)
    print(elem['prompt'])
    print(elem['image_paths'][0])
    urllib.request.urlretrieve(elem['image_paths'][0], 'imgs/{}.jpg'.format(index))

# Format Images
print('# Format Images')
for idx, key in enumerate(dict.items()):
    print(idx)
    image = Image.open('imgs/{}.jpg'.format(idx))
    ImageOps.fit(image, (1080, 1350)).save('imgs/{}.jpg'.format(idx))

# Store CSV
print('# Store CSV')
with open('imgs/dict.csv','w') as myfile:
    myfile.truncate()
    w = csv.writer(myfile)
    for key, val in dict.items():
        print(key)
        w.writerow([key,val])
    myfile.flush()

# Login to instagram
print('# Login to instagram')
cl = Client()
cl.login(client, secret)

# Read from CSV and Publish to instagram
print('# Read from CSV and Publish to instagram')
csvreader = csv.reader(open('imgs/dict.csv'))
for row in csvreader:
    print(row[0])
    cl.photo_upload("imgs/{}".format(row[0]),
                    row[1],
                    extra_data={
                        "custom_accessibility_caption": row[1],
                        "like_and_view_counts_disabled": 0,
                        "disable_comments": 0
                    }
    )
