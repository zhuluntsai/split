import json
import os
import argparse
import pathlib
import shutil
import sys
import copy
import numpy as np
import datetime
import math
from tqdm import tqdm

# i: index for images, j: index for annotations

original_folder_path = str(pathlib.Path().absolute())
train_folder_path = original_folder_path + "/training_data"
test_folder_path = original_folder_path + "/testing_data"
images_folder_path = original_folder_path + "/images"
labels_folder_path = original_folder_path + "/labels"

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }
images_list = [ ]

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter, description= '''\
 description:

    - program will: combine json --> area filter --> split json (optional) --> convert to yolo (optional)
    
    - type -s or -y to determine the final format
    - type -tr to set the train ratio

    - default parameter: 
    
        train_ratio: 0.8
    ''')

    parser.add_argument("-s", "--split", help= "split json", action = "store_true")
    parser.add_argument("-y", "--convert_to_yolo", help= "convert to yolo format", action = "store_true")
    parser.add_argument("-f", "--filter", help= "area filter", action = "store_true")

    parser.add_argument("-tr", "--train_ratio", help= "ratio of training data, default= 0.8", type= float, default= 0.8)

    arg = parser.parse_args()

    return arg

def combine():

    combine_json = copy.deepcopy(empty_json)
    # rename_list = open(f"rename_list_combine.txt", "w")
    category_dict = { }

    category_dict = collect_category(category_dict)

    i = 0
    j = 0
    k = 1
    accumulate = 0

    for item in os.listdir():
        if item.endswith('.json'): #and item != "0.json":

            old_json = normalize(json.load(open(item, "r")), item)

            old_category_dict = { }

            for l, categories in enumerate(old_json['categories']):
                old_category_dict.update({categories['name'] : l})

            key_list = list(old_category_dict.keys())
            val_list = list(old_category_dict.values())

            # append 'images' and rename the file name of pictures
            print(f' {item}')
            for images in tqdm(old_json['images']):
                i += 1
                for annotations in old_json['annotations']:
                    if annotations['image_id'] == images['id']:
                        j += 1
                        annotations['id'] = f"temp_{j:>06}"

                        annotations['segmentation'] = [ ]
                        annotations['image_id'] = f"temp_{i:>06}"
                        annotations['category_id'] = category_dict[key_list[val_list.index(annotations['category_id'] - 1)]]
                        combine_json['annotations'].append(annotations)

                images['id'] = f"temp_{i:>06}"
                try:
                    os.rename(images['file_name'], f'temp_{i:>06}.jpg')
                except:
                    pass
                # rename_list.write(images['file_name'] + f' / {i:>06}.jpg \n')
                images['file_name'] = f'temp_{i:>06}.jpg'
                combine_json['images'].append(images)

            os.remove(item)
    
    # append 'categories'
    for i, categories in enumerate(category_dict):
        category_content = {
            "supercategory": "none",
            "id": i + 1,
            "name": categories}

        combine_json['categories'].append(category_content)

    with open('0.json', 'w') as outfile:
        json.dump(combine_json, outfile, indent = 2, ensure_ascii = False)

    # rename_list.close()

def filterr():

    area_filter_json = copy.deepcopy(empty_json)
    j = 0

    for item in os.listdir():
        if item == "0.json":
            all_json = json.load(open(item, "r"))

    amount_list, category_list = count_annotations(all_json)

    print(' enter category id you want to keep, and split by space')
    category_id_list = list(map(int, input().split(' ')))
    print(' enter the ratio of each category, and split by space')
    category_amount_list = list(map(float, input().split(' ')))

    if len(category_id_list) != len(category_amount_list):
        print("input category id and ratio doesn't match")
        exit()

    print(' id\tinstance amount\t\tname')
    for i in range(len(category_id_list)):
        category_amount_list[i] *= amount_list[category_id_list[i] - 1] 
        print(f" {category_id_list[i]}\t{amount_list[category_id_list[i]-1]} >> {math.floor(category_amount_list[i])}\t\t{category_list[category_id_list[i]-1]}")    

    for annotations in all_json['annotations']:
        is_pass = True

        if annotations['category_id'] in category_id_list:
            index = category_id_list.index(annotations['category_id'])
            if category_amount_list[index] >= 0:
                category_amount_list[index] -= 1
                area_filter_json['annotations'].append(annotations)
                images_list.append(annotations["image_id"])

    for images in all_json['images']:
        is_pass = False
        
        # check images['id'] is in the images_list
        for image_id in set(images_list):
            if image_id == images['id']:
                is_pass = True
                images_list.remove(image_id)
                area_filter_json['images'].append(images)
                break

        # if images['id'] is not in the images_list
        if not is_pass:
            try:
                os.remove(images['id'] + ".jpg")
            except:
                pass
            
    for categories in all_json['categories']:
        if categories['id'] in category_id_list: 
            area_filter_json['categories'].append(categories)

    with open('0.json', 'w') as outfile:
        json.dump(area_filter_json, outfile, indent = 2, ensure_ascii = False)

    # normalize
    combine()

def split(usage: str, folder_path: str, file_name):

    all_json = json.load(open("0.json", "r"))
    data = copy.deepcopy(empty_json)
    # rename_list = open(f"rename_list_{usage}.txt", "w")

    i = 0
    j = 0
    accumulate = 1
    print(f' creating {usage} data')
    for target_file_name in tqdm(file_name):

        # match target file name and file name in 0.json
        for images in all_json['images']:
            if target_file_name == images['file_name']:
                i += 1
                images['id'] = i

                os.rename(folder_path + "/" + images['file_name'], folder_path + "/" + f'{i:>06}.jpg')
                # rename_list.write(images['file_name'] + f' / {i:>06}.jpg \n')
                images['file_name'] = f'{i:>06}.jpg'
                data['images'].append(images)
                
                continue

        for annotations in all_json['annotations']:
            if target_file_name == f"{annotations['image_id']:>06}.jpg":
                j += 1
                annotations['id'] = j 

                annotations['image_id'] = accumulate
                annotations['iscrowd'] = 0
                annotations['area'] = annotations['bbox'][2] * annotations['bbox'][3]
                data['annotations'].append(annotations)

                # print(target_file_name + "/" + str(j) + "/" + str(accumulate))

                continue

        accumulate += 1

    for categories in all_json['categories']:
        data['categories'].append(categories)

    with open(original_folder_path + f'/{usage}_data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 2, ensure_ascii = False)

    # rename_list.close()
    
    return i, j

def convert(usage: str, folder_path: str, file_name):

    all_json = json.load(open("0.json", "r"))
    # file_name_list_txt = open(f"{usage}.txt", 'w')

    i = 0
    j = 0

    for target_file_name in file_name:

        # match target file name and file name in 0.json
        for images in all_json['images']:
            if target_file_name == images['file_name']:
                i += 1
                os.rename(folder_path + "/" + images['file_name'], folder_path + "/" + images['file_name'][5:])

                # file_name_list_txt.write(f"custom_data/images/{images['id']:>06}.jpg\n")
                yolo_format_txt = open(f"labels/{images['id']:>06}.txt", 'w')

                for annotations in all_json['annotations']:
                    if str(annotations['image_id']) == f"{str(images['id']):>06}":
                        j += 1
                        object_center_in_x = ((annotations['bbox'][0] + annotations['bbox'][2]) / 2) / images['width']
                        object_center_in_y = ((annotations['bbox'][1] + annotations['bbox'][3]) / 2) / images['height']
                        object_width = annotations['bbox'][2] / images['width']
                        object_height = annotations['bbox'][3] / images['height']

                        yolo_format_txt.write(f"{int(annotations['category_id']) - 1} {object_center_in_x} {object_center_in_y} {object_width} {object_height}\n")

                yolo_format_txt.close()

    # file_name_list_txt.close()

    return i, j

def result(arg, output_type: str):
    result_txt = open(f"result_{output_type}.txt", "w")

    result_txt.write(f'''\
 time: {datetime.datetime.now()}
 output type: {output_type}

    train images amount: {train_images_amount}
    train labels amount: {train_labels_amount}

    test images amount: {test_images_amount}
    test labels amount: {test_labels_amount}

    train ratio: {arg.train_ratio}
    ''')

    result_txt.close()

def random_file_name(arg):

    # pylint: disable = unbalanced-tuple-unpacking

    all_file_name = []

    for item in os.listdir(original_folder_path):
        if item.endswith('.jpg'):
            all_file_name.append(item)

    np.random.shuffle(all_file_name)
    train_amount = int(len(all_file_name) * float(arg.train_ratio))
    train_file_name, test_file_name = np.split(np.array(all_file_name), [train_amount], 0)

    return train_file_name, test_file_name

def collect_category(category_dict):
    
    k = 1
    for item in os.listdir():
        if item.endswith('.json'):

            old_json = json.load(open(item, "r"))
            
            for categories in old_json['categories']:

                category_name = categories['name']
                if category_name not in category_dict:
                    category_dict.update({category_name : k})

                    category_content = {
                        "supercategory": "none",
                        "id": k,
                        "name": category_name}
                    k += 1

    return category_dict

def normalize(old_json, item):

    new_json = copy.deepcopy(empty_json)

    i = 0
    j = 0
    k = 0

    for categories in old_json['categories']:
        k += 1
        categories['original_id'] = categories['id']
        categories['id'] = k
        new_json['categories'].append(categories)

    for images in old_json['images']:
        i += 1
        images['original_id'] = images['id']
        images['id'] = i
        new_json['images'].append(images)

    for annotations in old_json['annotations']:
        j += 1
        annotations['id'] = j

        for images in old_json['images']:
            if images['original_id'] == annotations['image_id']:
                annotations['image_id'] = images['id']
                break

        for categories in old_json['categories']:
            if categories['original_id'] == annotations['category_id']:
                annotations['category_id'] = categories['id']
                break
        
        new_json['annotations'].append(annotations)      

    # with open(f'{item}_normalize.json', 'w') as outfile:
    #     json.dump(new_json, outfile, indent = 2, ensure_ascii = False) 
    
    return new_json

def count_annotations(json):
    amount_list = []
    category_list = []

    for categories in json['categories']:
        amount_list.append(0)
    amount_list.append(0)

    for annotations in json['annotations']:
        amount_list[annotations['category_id'] - 1] += 1

    print(' id\tinstance amount\t\tname')
    for categories in json['categories']:
        category_list.append(categories['name'])
        print(f" {categories['id']}\t{amount_list[categories['id'] - 1]}\t\t\t{categories['name']}")
    
    return amount_list, category_list

if __name__ == "__main__":

    #start
    arg = create_parser()
    print(f"\n train ratio: {arg.train_ratio}")

    skip_combine = False
    for item in os.listdir():
        if item == "0.json":
            skip_combine = True

    if skip_combine == False:     
        combine()
        print(" jsons have been combined")

    if arg.filter == True:
        filterr()
        print(" json has been filtered")

    #body
    train_file_name, test_file_name = random_file_name(arg)

    if arg.split == True:
        os.mkdir(train_folder_path)
        os.mkdir(test_folder_path)

        for item in train_file_name:
            shutil.copy(original_folder_path + "/" + item, train_folder_path + "/" + item)

        for item in test_file_name:
            shutil.copy(original_folder_path + "/" + item, test_folder_path + "/" + item)

        train_images_amount, train_labels_amount = split("training", train_folder_path, train_file_name)
        test_images_amount, test_labels_amount = split("testing", test_folder_path, test_file_name)

        print(" json has been split")

        # try:
        #     result(arg, "split")
        # except:
        #     pass

    if arg.convert_to_yolo == True:
        os.mkdir(images_folder_path)
        os.mkdir(labels_folder_path)

        for item in np.concatenate((train_file_name, test_file_name)):
            shutil.copy(original_folder_path + "/" + item, images_folder_path + "/" + item)

        train_images_amount, train_labels_amount = convert("training", images_folder_path, train_file_name)
        test_images_amount, test_labels_amount = convert("testing", images_folder_path, test_file_name)

        print(" format has been converted to yolo format")

        # try:
        #     result(arg, "yolo")
        # except:
        #     pass

    # end
    if arg.split == True or arg.convert_to_yolo == True:
        for item in os.listdir():
            if item.startswith('temp') or item == "0.json":
                os.remove(item)