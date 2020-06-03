from data_aug.data_aug import *
from data_aug.bbox_util import *
from cv2 import cv2
import pickle as pkl
import numpy as np 
import matplotlib.pyplot as plt
import json
from PIL import Image


all_json = json.load(open("0.json", "r"))
class_type = 0.

transforms = Sequence([RandomHorizontalFlip(1), RandomScale(0.2, diff = True), RandomRotate(10)])

for images in all_json['images']:
    print(images['file_name'])
    image = cv2.imread(images['file_name'])[:,:,::-1]
    bbox_list = []

    for annotations in all_json['annotations']:
        if images['id'] == annotations['image_id']:
            bbox_list.append([annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3], class_type])
    
    image, bbox_nparray = transforms(image, np.array(bbox_list))

    image = draw_rect(image, bbox_nparray)
    image = Image.fromarray(image, 'RGB') 
    image.save(images['file_name'])

    k = -1

    for annotations in all_json['annotations']:
        if images['id'] == annotations['image_id']:
            k += 1
            annotations['bbox'] = bbox_list[k]

with open('0.json', 'w') as outfile:
        json.dump(all_json, outfile, indent = 2, ensure_ascii = False)