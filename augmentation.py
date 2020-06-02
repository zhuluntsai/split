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
annotation_list = []
image_list = []

for images in all_json['images']:
    image_list.append(images['file_name'])

for annotations in all_json['annotations']:
    annotation_list.append([annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3], class_type])
    break
    
# annotation_list = np.asarray(annotation_list)
img = cv2.imread("temp_00025.jpg")[:,:,::-1]
# bboxes = pkl.load(open("messi_ann.pkl", "rb"))
bboxes = np.array(annotation_list)
print(bboxes)

transforms = Sequence([RandomHorizontalFlip(1), RandomScale(0.2, diff = True), RandomRotate(10)])

img, bboxes = transforms(img, bboxes)

image = Image.fromarray(img, 'RGB')
image.save('my.png')
image.show()

print(type(img))
print(bboxes)
# plt.imshow(draw_rect(img, bboxes))
plt.imshow(img)
# plt.show()
plt.savefig("temp_00025.jpg")