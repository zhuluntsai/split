import json
import os
import argparse
import pathlib
import shutil
import sys
import copy
import numpy as np
import datetime

# i: index for images, j: index for annotations

original_folder_path = str(pathlib.Path().absolute())
train_folder_path = original_folder_path + "/training_data"
test_folder_path = original_folder_path + "/testing_data"
images_folder_path = original_folder_path + "/images"
labels_folder_path = original_folder_path + "/labels"

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [ { "supercategory": "none", "id": 1, "name": "hole"} ] }

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter, description= '''\
 description:

    - the program will: combine json --> area filter --> split json (optional) --> convert to yolo (optional)
    - type -s or -y to decide the final format
    - type -tr or -aft to set the train ratio or area filter ratio
    - remember keep images, jsons, and split.py in the same folder.
    ''')

    parser.add_argument("-s", "--split", help= "split json", action = "store_true")
    parser.add_argument("-y", "--convert_to_yolo", help= "convert to yolo format", action = "store_true")

    parser.add_argument("-tr", "--train_ratio", help= "ratio of training data, default= 0.8", type= float, default= 0.8)
    parser.add_argument("-afr", "--area_filter_ratio", help= "ratio of area in a picture, default=0.3", type= float, default=0.3)

    arg = parser.parse_args()

    return arg

def combine():

    combine_json = copy.deepcopy(empty_json)

    i = 0
    j = 0
    accumulate = 0

    for item in os.listdir():
        if item.endswith('.json') and item != "0.json":

            old_json = json.load(open(item, "r"))

            # append 'images' and rename the file name of pictures
            for images in old_json['images']:
                i += 1
                images['id'] = i

                os.rename(images['file_name'], f'temp_{i:>05}.jpg')
                images['file_name'] = f'temp_{i:>05}.jpg'
                combine_json['images'].append(images)

            # append 'annotations'
            for annotations in old_json['annotations']:
                j += 1
                annotations['id'] = j 
                
                annotations['image_id'] = "temp_" + str(f"{annotations['image_id'] + accumulate:>05}")
                combine_json['annotations'].append(annotations)

            accumulate += len(old_json['images'])
            os.remove(item)

    with open('0.json', 'w') as outfile:
        json.dump(combine_json, outfile, indent = 2, ensure_ascii = False)

def area_filter(arg):

    area_filter_json = copy.deepcopy(empty_json)
    j = 0
    k = 0
    pass_area_filter = False

    for item in os.listdir():
        if item == "0.json":

            all_json = json.load(open(item, "r"))

            for images in all_json['images']:
                all_area = images['height'] * images['width']

                for annotations in all_json['annotations']:

                    # match image id and filter area smaller than area ratio
                    if str(annotations['image_id']) == f"temp_{str(images['id']):>05}" and annotations['area'] / all_area <= arg.area_filter_ratio:
                        pass_area_filter = True
                        j += 1
                        annotations['id'] = j

                        area_filter_json['annotations'].append(annotations)
                
                # append image pass area filter
                if pass_area_filter == True:
                    area_filter_json['images'].append(images)
                    pass_area_filter = False
                else:
                    os.remove(f"temp_{str(images['id']):>05}.jpg")

    with open('0.json', 'w') as outfile:
        json.dump(area_filter_json, outfile, indent = 2, ensure_ascii = False)

def split(usage: str, folder_path: str, file_name):

    all_json = json.load(open("0.json", "r"))
    data = copy.deepcopy(empty_json)

    i = 0
    j = 0
    accumulate = 1

    for target_file_name in file_name:

        # match target file name and file name in 0.json
        for images in all_json['images']:
            if target_file_name == images['file_name']:
                i += 1
                images['id'] = i

                os.rename(folder_path + "/" + images['file_name'], folder_path + "/" + f'{i:>05}.jpg')
                images['file_name'] = f'{i:>05}.jpg'
                data['images'].append(images)
                
                continue

        for annotations in all_json['annotations']:
            if target_file_name == f"{annotations['image_id']:>05}.jpg":
                j += 1
                annotations['id'] = j 

                annotations['image_id'] = accumulate
                data['annotations'].append(annotations)

                # print(target_file_name + "/" + str(j) + "/" + str(accumulate))

                continue

        accumulate += 1

    with open(original_folder_path + f'/{usage}_data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 2, ensure_ascii = False)
    
    return i, j

def convert(usage: str, folder_path: str, file_name):

    all_json = json.load(open("0.json", "r"))
    file_name_list_txt = open(f"{usage}.txt", 'w')

    i = 0
    j = 0

    for target_file_name in file_name:

        # match target file name and file name in 0.json
        for images in all_json['images']:
            if target_file_name == images['file_name']:
                i += 1
                os.rename(folder_path + "/" + images['file_name'], folder_path + "/" + images['file_name'][5:])

                file_name_list_txt.write(f"images/{images['id']:>05}.jpg\n")
                yolo_format_txt = open(f"labels/{images['id']:>05}.txt", 'w')

                for annotations in all_json['annotations']:
                    if str(annotations['image_id']) == f"temp_{str(images['id']):>05}":
                        j += 1
                        object_center_in_x = ((annotations['bbox'][0] + annotations['bbox'][2]) / 2) / images['width']
                        object_center_in_y = ((annotations['bbox'][1] + annotations['bbox'][3]) / 2) / images['height']
                        object_width = annotations['bbox'][2] / images['width']
                        object_height = annotations['bbox'][3] / images['height']

                        yolo_format_txt.write(f"0 {object_center_in_x} {object_center_in_y} {object_width} {object_height}\n")

                yolo_format_txt.close()

    file_name_list_txt.close()

    return i, j

def result(arg):
    result_txt = open("result.txt", "w")

    result_txt.write(f'''\
 time: {datetime.datetime.now()}

    train images amount: {train_images_amount}
    train labels amount: {train_labels_amount}

    test images amount: {test_images_amount}
    test labels amount: {test_labels_amount}

    train ratio: {arg.train_ratio}
    area filter ratio: {arg.area_filter_ratio}
    ''')

    result_txt.close()

    os.remove("0.json")
    for item in os.listdir():
        if item.startswith('temp'):
            os.remove(item)

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

if __name__ == "__main__":

    #start
    arg = create_parser()
    print(f"\n train ratio: {arg.train_ratio} \n area filter ratio: {arg.area_filter_ratio} \n")

    combine()
    print(" jsons have been combined")

    area_filter(arg)
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

    if arg.convert_to_yolo == True:
        os.mkdir(images_folder_path)
        os.mkdir(labels_folder_path)

        for item in np.concatenate((train_file_name, test_file_name)):
            shutil.copy(original_folder_path + "/" + item, images_folder_path + "/" + item)

        train_images_amount, train_labels_amount = convert("training", images_folder_path, train_file_name)
        test_images_amount, test_labels_amount = convert("testing", images_folder_path, test_file_name)

        print(" format has been converted to yolo format")

    #end
    result(arg)
    