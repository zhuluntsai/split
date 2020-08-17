import argparse
import json
import cv2
import os
import pathlib

parser = argparse.ArgumentParser(description='ACID_json_debug')
parser.add_argument('--file', default='/home/hteam/Documents/hao/Research/ACID/ACID_Images', type=str, help='data file')
parser.add_argument('--label', default='/home/hteam/Documents/hao/Research/ACID/ACID.json', type=str, help='COCO format json')

def main():
    args = parser.parse_args()

    args.file = str(pathlib.Path().absolute())
    # args.label = str(pathlib.Path().absolute())

    with open(args.label) as f:
        label = json.load(f)

    ### modify h & w
    for i in range(len(label["images"])):  
        img_name = label["images"][i]
        img_path = os.path.join(args.file, img_name['file_name'])
        img = cv2.imread(img_path)
        img_height = img.shape[0]
        img_width = img.shape[1]
        label_height = img_name["height"]
        label_width = img_name["width"]
        if label_height != img_height:
            label["images"][i]["height"] = img_height
            print('image', i+1, 'height is wrong')
        if label_width != img_width:
            label["images"][i]["width"] = img_width
            print('image', i+1, 'width is wrong')
    
    with open(args.label, 'w') as g:
        json.dump(label, g)
    f.close()
    g.close()

if __name__ == '__main__':
    main()