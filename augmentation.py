from data_aug.data_aug import *
from data_aug.bbox_util import *
from cv2 import cv2
import numpy as np 
import matplotlib.pyplot as plt
import json
from PIL import Image


all_json = json.load(open("0.json", "r"))
class_type = 0.

transforms = Sequence([RandomTranslate()])
# RandomHorizontalFlip(1)
# RandomScale(0.3, diff = True)
# RandomTranslate(0.3, diff = True)
# RandomRotate(20)
# RandomShear(0.2)
# Resize(608)
# RandomHSV(100, 100, 100)

for images in all_json['images']:

    image = cv2.imread(images['file_name'])[:,:,::-1]
    bbox_list = []

    for annotations in all_json['annotations']:
        if images['id'] == annotations['image_id']:
            bbox_list.append([annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3], class_type])
    while 1:
        try:
            transformed_image, bbox_nparray = transforms(image, np.array(bbox_list))
            k = -1

            for annotations in all_json['annotations']:
                if images['id'] == annotations['image_id']:
                    k += 1
                    temp = bbox_nparray[k].tolist()
                    annotations['bbox'] = temp

        except:
            print(images['file_name'])
            continue

        break

    transformed_image = draw_rect(transformed_image, bbox_nparray)
    transformed_image = Image.fromarray(transformed_image, 'RGB') 
    transformed_image.save(images['file_name'])

with open('0.json', 'w') as outfile:
        json.dump(all_json, outfile, indent = 2, ensure_ascii = False)