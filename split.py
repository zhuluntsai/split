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

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }
annotations_list = [359, 370, 381, 382, 371, 379, 216, 218, 221, 224, 226, 229, 232, 235, 238, 241, 244, 247, 250, 287, 311, 335, 337, 341, 344, 347, 350, 354, 356, 259, 362, 365, 368, 372, 373, 414, 417, 383, 387, 384, 389, 386, 385, 388, 394, 390, 391, 392, 393, 432, 447, 448, 449, 450, 452, 451, 456, 455, 453, 458, 454, 457, 472, 479, 533, 540, 544, 697, 732, 865, 867, 777, 778, 780, 779, 781, 782, 784, 783, 785, 786, 787, 788, 789, 790, 791, 793, 796, 792, 794, 795, 797, 798, 799, 800, 604, 606, 607, 605, 609, 608, 611, 610, 621, 615, 612, 622, 614, 613, 616, 617, 618, 619, 620, 623, 624, 625, 626, 627, 1, 2, 3, 4, 9, 10, 7, 6, 8, 5, 13, 12, 11, 15, 16, 24, 18, 19, 14, 20, 17, 21, 23, 22, 848, 854, 853, 857, 855, 852, 847, 856, 851, 849, 858, 850, 26, 27, 35, 31, 37, 32, 36, 38, 39, 30, 507, 509, 514, 508, 510, 512, 506, 516, 521, 523, 525, 527, 529, 538, 531, 536, 423, 421, 427, 429, 435, 437, 441, 445, 443,   255, 252, 259, 279, 280, 276, 261, 283,      265, 267, 269, 271, 272, 274, 286,       307, 309, 293, 297, 299, 300, 313,      321, 325, 327, 330, 332, 318, 315, 317, 304,    303, 290, 464, 467,       489, 487, 459, 476, 492, 480, 498, 473, 484, 496, 502, 546, 548, 549, 550, 561, 560, 552, 553, 555, 566, 564, 567, 558, 556, 569, 568, 574, 573, 584, 583, 575, 577, 578,      586, 588, 579, 652, 659, 660, 658, 665, 664, 663, 667, 668, 669, 679, 678, 677, 674, 672, 673, 683, 682, 681, 695, 694, 693, 687, 686, 689, 690, 691, 685, 700, 701, 699,    883, 885, 884, 877, 875, 876, 881, 880, 879, 870, 871, 869, 874, 873, 872, 887, 888, 889, 890, 891, 892, 896, 897, 898, 901, 900, 899, 895, 894, 893, 45, 44, 43, 42, 41, 40, 53, 54, 52, 56, 57, 55, 47, 48, 46, 51, 50, 49, 68, 69, 70, 71, 72, 74, 63, 64, 65, 61, 60, 59, 80, 81, 82, 85, 89, 86, 75, 76, 77, 158, 160, 161, 153, 154, 155, 163, 164, 165, 183, 185, 186, 189, 190, 193, 197, 198, 200, 194, 168, 169, 170, 174, 178, 179, 732, 737, 734, 735, 724, 723, 752, 751, 748, 750, 749, 745, 743, 746, 835, 842, 841, 843, 845, 846, 837, 145, 146, 150, 102, 103, 96, 94, 101, 100, 90, 803, 809, 804, 808, 91, 92, ]
images_list = []
category_dict = { }

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
    rename_list = open(f"rename_list_combine.txt", "w")

    i = 0
    j = 0
    k = 1
    accumulate = 0

    for item in os.listdir():
        if item.endswith('.json') and item != "0.json":

            old_json = json.load(open(item, "r"))

            # append 'images' and rename the file name of pictures
            for images in old_json['images']:
                i += 1
                images['id'] = f"temp_{i:>05}"

                os.rename(images['file_name'], f'temp_{i:>05}.jpg')
                rename_list.write(images['file_name'] + f' / {i:>05}.jpg \n')
                images['file_name'] = f'temp_{i:>05}.jpg'
                combine_json['images'].append(images)

            # append 'annotations'
            for annotations in old_json['annotations']:  
                j += 1
                annotations['id'] = f"temp_{j:>05}"
                
                annotations['image_id'] = f"temp_{annotations['image_id'] + accumulate:>05}"
                combine_json['annotations'].append(annotations)

            # append 'categories'
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

            accumulate += len(old_json['images'])
            os.remove(item)

    with open('0.json', 'w') as outfile:
        json.dump(combine_json, outfile, indent = 2, ensure_ascii = False)

    rename_list.close()

def filter(arg):

    area_filter_json = copy.deepcopy(empty_json)
    j = 0

    for item in os.listdir():
        if item == "0.json":
            all_json = json.load(open(item, "r"))

    for annotations in all_json['annotations']:
        is_pass = True

        # check annotations['id'] is in the annotations_list
        for annotation_id in annotations_list:
            if annotations['id'] == f"temp_{annotation_id:>05}":
                is_pass = False
                annotations_list.remove(annotation_id)

        # if annotations['id'] is not in the annotations_list
        if is_pass: 
            j += 1
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

        # if images['id'] is not in the images_list
        if not is_pass:
            os.remove(images['id'] + ".jpg")

    for categories in all_json['categories']:
        area_filter_json['categories'].append(categories)

    with open('0.json', 'w') as outfile:
        json.dump(area_filter_json, outfile, indent = 2, ensure_ascii = False)

def split(usage: str, folder_path: str, file_name):

    all_json = json.load(open("0.json", "r"))
    data = copy.deepcopy(empty_json)
    rename_list = open(f"rename_list_{usage}.txt", "w")

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
                rename_list.write(images['file_name'] + f' / {i:>05}.jpg \n')
                images['file_name'] = f'{i:>05}.jpg'
                data['images'].append(images)
                
                continue

        for annotations in all_json['annotations']:
            if target_file_name == f"{annotations['image_id']:>05}.jpg":
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

    rename_list.close()
    
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

                file_name_list_txt.write(f"custom_data/images/{images['id']:>05}.jpg\n")
                yolo_format_txt = open(f"labels/{images['id']:>05}.txt", 'w')

                for annotations in all_json['annotations']:
                    if str(annotations['image_id']) == f"{str(images['id']):>05}":
                        j += 1
                        object_center_in_x = ((annotations['bbox'][0] + annotations['bbox'][2]) / 2) / images['width']
                        object_center_in_y = ((annotations['bbox'][1] + annotations['bbox'][3]) / 2) / images['height']
                        object_width = annotations['bbox'][2] / images['width']
                        object_height = annotations['bbox'][3] / images['height']

                        yolo_format_txt.write(f"{int(annotations['category_id']) - 1} {object_center_in_x} {object_center_in_y} {object_width} {object_height}\n")

                yolo_format_txt.close()

    file_name_list_txt.close()

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

if __name__ == "__main__":

    #start
    arg = create_parser()
    print(f"\n train ratio: {arg.train_ratio}")

    skip_combine_and_filter = False
    for item in os.listdir():
        if item == "0.json":
            skip_combine_and_filter = True

    if skip_combine_and_filter == False:     
        combine()
        print(" jsons have been combined")

    if arg.filter == True:
        filter(arg)
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

        try:
            result(arg, "split")
        except:
            pass

    if arg.convert_to_yolo == True:
        os.mkdir(images_folder_path)
        os.mkdir(labels_folder_path)

        for item in np.concatenate((train_file_name, test_file_name)):
            shutil.copy(original_folder_path + "/" + item, images_folder_path + "/" + item)

        train_images_amount, train_labels_amount = convert("training", images_folder_path, train_file_name)
        test_images_amount, test_labels_amount = convert("testing", images_folder_path, test_file_name)

        print(" format has been converted to yolo format")

        try:
            result(arg, "yolo")
        except:
            pass

    # end
    if arg.split == True or arg.convert_to_yolo == True:
        for item in os.listdir():
            if item.startswith('temp') or item == "0.json":
                os.remove(item)