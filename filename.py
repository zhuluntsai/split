import json
import os
import copy
import argparse

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }
category_dict = { }

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--filename", type=str)
    parser.add_argument("-s", "--start", type=int)
    parser.add_argument('-i', '--image_path', type=str, default='')
    arg = parser.parse_args()

    return arg


arg = create_parser()
combine_json = copy.deepcopy(empty_json)
old_json = json.load(open(arg.filename, "r"))
path = arg.image_path

i = arg.start + len(old_json['images'])
k = 1

old_json['images'].reverse()

for images in old_json['images']:
    i -= 1
    # print(images['file_name'] + '>>>>>' + f'{i:>06}.jpg')
    
    os.rename(path + images['file_name'], path + f'{i:>06}.jpg')


    images['file_name'] = f'{i:>06}.jpg'
    combine_json['images'].append(images)

combine_json['images'].reverse()


for annotations in old_json['annotations']:      
    combine_json['annotations'].append(annotations)

for categories in old_json['categories']:

    category_name = categories['name']
    if category_name not in category_dict:
        category_dict.update({category_name : k})

        category_content = {
            "supercategory": "none",
            "id": k,
            "name": category_name}

        combine_json['categories'].append(category_content)

        k += 1

with open(arg.filename, 'w') as outfile:
        json.dump(combine_json, outfile, indent = 2, ensure_ascii = False)