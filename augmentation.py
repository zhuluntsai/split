from data_aug.data_aug import *
from data_aug.bbox_util import *
from cv2 import cv2
import numpy as np 
import matplotlib.pyplot as plt
import json
from PIL import Image
import random

all_json = json.load(open("0.json", "r"))
class_type = 0.

random_number = random.randint(1, 3)
random_sequence = random.sample( [ RandomHorizontalFlip(0.5), RandomScale(0.1, diff = True), RandomTranslate(0.1, diff = True), RandomRotate(3), RandomShear(0.2), RandomHSV(10, 10, 10) ] , random_number)
transforms = Sequence(random_sequence)

for images in all_json['images']:

    print(images['file_name'])
    image = cv2.imread(images['file_name'])[:,:,::-1]
    bbox_list = []

    for annotations in all_json['annotations']:
        if images['id'] == annotations['image_id']:
            bbox_list.append([annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3], class_type])
    
    # if whole bbox is out of the image, program will retransform it until all bboxes are in the image
    while 1:
        try:
            transformed_image, bbox_nparray = transforms(image, np.array(bbox_list))
            k = -1

            for annotations in all_json['annotations']:
                if images['id'] == annotations['image_id']:
                    k += 1

                    # avoid use the wrong annotations['bbox'] before the index error occuring
                    temp = bbox_nparray[k].tolist()
                    annotations['bbox'] = temp
        except:
            continue
        break

    # transformed_image = draw_rect(transformed_image, bbox_nparray)

    # transfer array to image
    transformed_image = Image.fromarray(transformed_image, 'RGB') 
    transformed_image.save(images['file_name'])

with open('0.json', 'w') as outfile:
    json.dump(all_json, outfile, indent = 2, ensure_ascii = False)