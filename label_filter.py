import json
import copy
import os

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }
label_filter_json = copy.deepcopy(empty_json)
images_list = []

for item in os.listdir():
    if item == "0.json":
        all_json = json.load(open(item, "r"))

for annotations in all_json['annotations']:
    if annotations['category_id'] == 5:
        annotations['category_id'] = 1
        label_filter_json['annotations'].append(annotations)
        images_list.append(annotations["image_id"])        

for images in all_json['images']:    
    is_pass = False

    for image_id in set(images_list):
        if image_id == images['id']:
            is_pass = True
            images_list.remove(image_id)
            label_filter_json['images'].append(images)

    if not is_pass:
        os.remove(images['id'] + ".jpg")

for categories in all_json['categories']:
    categories['name'] = "mobile_crane"
    label_filter_json['categories'].append(categories)
    break

with open('0.json', 'w') as outfile:
    json.dump(label_filter_json, outfile, indent = 2, ensure_ascii = False)