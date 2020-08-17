import json
import copy
import os
import pathlib

empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }

category_name_dict = { }
category_name_index = 1

i = 1
for item in os.listdir():
    if item.endswith('.json') and item != "new.json":

        print(item)
        new_json = copy.deepcopy(empty_json)
        original_json = json.load(open(item, "r"))

        new_json['images'].append({
            "file_name": original_json['annotation']['filename'], 
            "height": int(original_json['annotation']['size']['height']), 
            "width": int(original_json['annotation']['size']['width']), 
            "id": i})

        j = 0

        try:
            for annotation_object in original_json['annotation']['object']:

                xmin = int(annotation_object['bndbox']["xmin"])
                ymin = int(annotation_object['bndbox']['ymin'])
                xmax = int(annotation_object['bndbox']['xmax'])
                ymax = int(annotation_object['bndbox']['ymax'])

                category_name = annotation_object['name']
                if category_name not in category_name_dict:
                    category_name_dict.update({category_name : category_name_index})
                    category_name_index += 1

                new_json['annotations'].append({
                    "image_id": i,
                    "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                    "category_id": category_name_dict[category_name],
                    "id": j})
                
                j += 1
        except:
            xmin = int(original_json['annotation']['object']['bndbox']["xmin"])
            ymin = int(original_json['annotation']['object']['bndbox']['ymin'])
            xmax = int(original_json['annotation']['object']['bndbox']['xmax'])
            ymax = int(original_json['annotation']['object']['bndbox']['ymax'])

            category_name = original_json['annotation']['object']['name']
            if category_name not in category_name_dict:
                category_name_dict.update({category_name : category_name_index})
                category_name_index += 1

            new_json['annotations'].append({
                "image_id": i,
                "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                "category_id": category_name_dict[category_name],
                "id": j})
            
            j += 1

        for category_name_dict_key in category_name_dict:

            category_content = {
                "supercategory": "none",
                "id": category_name_dict[category_name_dict_key],
                "name": category_name_dict_key}

            new_json['categories'].append(category_content)

        with open(item, 'w') as outfile:
                json.dump(new_json, outfile, indent = 2, ensure_ascii = False)