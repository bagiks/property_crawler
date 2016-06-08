import json
from pprint import pprint
import os
import urllib

with open("../../data/output2.json") as data_file:
    data = json.load(data_file)

home_dir = os.path.dirname(os.path.realpath(__file__))

for d in data:
    dir_path = os.path.join(home_dir+"/data/", d['directory'][0])

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for i in d['image_urls']:
        img_name = i.split("/")[-1]
        img_folder_path = os.path.join(dir_path,img_name.split(".")[0])
        annotation_name = img_name.replace("jpg","xml")
        annotation_link = i.replace("Images","Annotations").replace("jpg","xml")

        os.mkdir(img_folder_path)
        urllib.urlretrieve(i, os.path.join(img_folder_path, img_name))
        urllib.urlretrieve(annotation_link, os.path.join(img_folder_path, annotation_name))











