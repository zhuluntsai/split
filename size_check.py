from PIL import Image
import os
import json

jpg_list = []
json_list = []

for jpg_item in os.listdir():
    if jpg_item.endswith('.jpg'):
        jpg_list.append(jpg_item)

for json_item in os.listdir():
    if json_item.endswith('.json'):
        json_list.append(json_item)

if len(json_list) == 1:

    all_json = json.load(open(json_list[0], "r"))

    for jpg_item in jpg_list:
        for images in all_json['images']:
            if (jpg_item == images['file_name']):

                im = Image.open(jpg_item)
                jpg_width, jpg_height = im.size

                json_width = images['width']
                json_height = images['height']
                # print(str(jpg_width) + " / " + str(json_width))
                if jpg_width != json_width:
                    print(jpg_item)
                    print(str(jpg_width) + " / " + str(json_width))
                    print("------------")
                
                if jpg_height != json_height:
                    print(jpg_item)
                    print(str(jpg_height) + " / " + str(json_height))
                    print("------------")

                # jpg_list.remove(jpg_item)
                # json_list.remove(json_item)
else:
    for jpg_item in jpg_list:
        for json_item in json_list:
            if (jpg_item[0:5] == json_item[0:5]):

                im = Image.open(jpg_item)
                jpg_width, jpg_height = im.size

                all_json = json.load(open(json_item, "r"))
                json_width = all_json['images'][0]['width']
                json_height = all_json['images'][0]['height']
                print(str(jpg_width) + " / " + str(json_width))

                if jpg_width != json_width:
                    print(jpg_item)
                    print(str(jpg_width) + " / " + str(json_width))
                    print("------------")
                
                if jpg_height != json_height:
                    print(jpg_item)
                    print(str(jpg_height) + " / " + str(json_height))
                    print("------------")

                # jpg_list.remove(jpg_item)
                # json_list.remove(json_item)