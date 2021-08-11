from data_aug.data_aug import *
from data_aug.bbox_util import *
from cv2 import cv2
import numpy as np 
import matplotlib.pyplot as plt
import json
from PIL import Image
import random
import argparse
from tqdm import tqdm

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter, description= '''\
 description:

    - program will randomly choose 1~3 type of augmentation method 
    
    - type -f to set the file name
    - type -r to draw rectangle
    
    - default parameter: 
    
        flip: 0.5
        scale: 0.1, scale_diff: True
        translate: 0.1, translate_diff: True
        rotate: 3
        shear: 0.1
        hsv: 10, 10, 10
    ''')

    parser.add_argument("-f", "--file_name", help= "json file name", type= str)
    parser.add_argument("-n", "--aug_times", help= "times of augmentation", type= int, default=5)
    parser.add_argument("-r", "--draw_rectangle", help= "draw rectangle", action = "store_true")
    parser.add_argument('-i', '--image_path', type=str, default='')

    parser.add_argument("-flip", help= "RandomHorizontalFlip", type= float, default= 0.5)
    parser.add_argument("-scale", help= "RandomScale", type= float, default= 0.1)
    parser.add_argument("-scale_diff", help= "RandomScale", default= True)
    parser.add_argument("-translate", help= "RandomTranslate", type= float, default= 0.1)
    parser.add_argument("-translate_diff", help= "RandomTranslate", default= True)
    parser.add_argument("-rotate", help= "RandomRotate", type= int, default= 3)
    parser.add_argument("-shear", help= "RandomShear", type= float, default= 0.1)
    parser.add_argument("-hsv", help= "RandomHSV", default= [10, 10, 10], nargs= 3)

    arg = parser.parse_args()
    return arg

arg = create_parser()

path = arg.image_path
augmentation_times = arg.aug_times

# print(f'''\

#     all parameter: 
#         flip: {arg.flip}
#         scale: {arg.scale}, scale_diff: {arg.scale_diff}
#         translate: {arg.translate}, translate_diff: {arg.translate_diff}
#         rotate: {arg.rotate}
#         shear: {arg.shear}
#         hsv: {arg.hsv[0]}, {arg.hsv[1]}, {arg.hsv[2]}

# augmentation times: {augmentation_times}
#     ''')

print(f' augmentation times: {augmentation_times}')

image_amount = 0
# image_amount_limitation = 800
for times in range(1, augmentation_times + 1):

    all_json = json.load(open(arg.file_name, "r"))
    random_number = random.randint(1, 3)
    random_sequence = random.sample( [ RandomHorizontalFlip(arg.flip), 
                                        RandomScale(arg.scale, diff = arg.scale_diff), 
                                        RandomTranslate(arg.translate, diff = arg.translate_diff), 
                                        RandomRotate(arg.rotate), 
                                        RandomShear(arg.shear), 
                                        RandomHSV(int(arg.hsv[0]), int(arg.hsv[1]), int(arg.hsv[2])) 
                                        ] , random_number)
    transforms = Sequence(random_sequence)

    # create the hint message
    random_sequence_to_str = ', '.join(str(random)[19:].split(' ')[0] for random in random_sequence)
    print(f'augmentation method : {random_sequence_to_str}')

    for images in tqdm(all_json['images']):

        # if image_amount > image_amount_limitation:
        #     break

        image = cv2.imread(path + images['file_name'])[:,:,::-1]
        images['file_name'] = f"{images['file_name'][:-4]}_{times}.jpg"
        bbox_list = []

        for annotations in all_json['annotations']:
            if images['id'] == annotations['image_id']:
                bbox_list.append([annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3], float(annotations['category_id'] - 1)])
        
        if len(bbox_list) != 0:
            image_amount += 1
            # if whole bbox is out of the image, program will retransform it until all bboxes are in the image
            try:
                while 1:
                    try:
                        transformed_image, bbox_nparray = transforms(image, np.array(bbox_list))
                        k = -1

                        for annotations in all_json['annotations']:
                            if images['id'] == annotations['image_id']:
                                k += 1

                                # avoid use the wrong annotations['bbox'] before the index error occuring
                                temp = bbox_nparray[k].tolist()
                                bbox = [temp[0], temp[1], temp[2] - temp[0], temp[3] - temp[1]]
                                # if all(b >= 0 for b in bbox):
                                annotations['bbox'] = bbox
                                # else:
                                #     annotations['bbox'] = [0, 0, 0, 0]

                    except:
                        continue
                    break
            except KeyboardInterrupt:
                break

            if arg.draw_rectangle == True:
                transformed_image = draw_rect(transformed_image, bbox_nparray)

            # transfer array to image
            transformed_image = Image.fromarray(transformed_image, 'RGB') 
            transformed_image.save(path + images['file_name'])

    with open(f"{arg.file_name[:-5]}_{times}.json", 'w') as outfile:
        json.dump(all_json, outfile, indent = 2, ensure_ascii = False)

    # if image_amount > image_amount_limitation:
    #     break