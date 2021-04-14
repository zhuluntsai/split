from PIL import Image, ImageEnhance
import os, random, json
import numpy as np

path = '/Users/weiluntsai/Desktop/桌面/CAE/synthestic_data/'
empty_json = {"images": [], "type": "instances", "annotations": [], "categories": [] }

background_images = [Image.open(path + 'background/' + x) for x in os.listdir(path + 'background/') if x.endswith('jpg')]
traffic_cone_images = [Image.open(path + 'traffic_cone/' + x) for x in os.listdir(path + 'traffic_cone/')]
crane_images = [Image.open(path + 'crane/' + x) for x in os.listdir(path + 'crane/')]

# widths, heights = zip(*(i.size for i in images))

# background_image = Image.open(path + '000232.jpg').convert('RGB')
# foreground_image = Image.open(path + '000213.tiff').convert('RGBA')

for i, background_image in enumerate(background_images):
    background_width, background_height = background_image.size

    image_content = {
            'file_name': f'{i:>05}.jpg',
            'height': background_height,
            'width': background_width,
            'id': i,
        }

    empty_json['images'].append(image_content)

    for k, crane_image in enumerate(crane_images):
        crane_width, crane_height = crane_image.size

        angle = random.uniform(-3, 3)
        resize_ratio = random.uniform(1.0, 2.0)
        brightness = random.uniform(1.2, 1.2)

        enhancer = ImageEnhance.Brightness(crane_image)
        crane_image = enhancer.enhance(brightness).rotate(angle, expand=1).resize((int(crane_image.width*resize_ratio), int(crane_image.height*resize_ratio)))
        crane_width, crane_height = crane_image.size
        
        crane_x = int(random.uniform(0, background_width - crane_width))
        crane_y = int(random.uniform(0, background_height - crane_height))
        background_image.paste(crane_image,box=(crane_x, crane_y),mask=crane_image)

        annotation_content = {
            'segmentation': [],
            'area': crane_height * crane_width,
            'iscrowd': 0,
            'image_id': i,
            'bbox': [crane_x, crane_y, crane_width, crane_height],
            'category_id': 1,
            'id': k,
            'ignore': 0,
        }

        empty_json['annotations'].append(annotation_content)

    traffic_cone_amount = int(random.uniform(len(traffic_cone_images)/2, len(traffic_cone_images)))
    for j, traffic_cone_image in enumerate(random.sample(traffic_cone_images, traffic_cone_amount)):

        angle = random.uniform(-5, 5)
        resize_ratio = random.uniform(0.8, 1.5)
        brightness = random.uniform(0.80, 1.0)

        enhancer = ImageEnhance.Brightness(traffic_cone_image)
        traffic_cone_image = enhancer.enhance(brightness).rotate(angle, expand=1).resize((int(traffic_cone_image.width*resize_ratio), int(traffic_cone_image.height*resize_ratio)))
        traffic_cone_width, traffic_cone_height = traffic_cone_image.size
        
        x = int(random.uniform(0, background_width - traffic_cone_width))
        y = int(random.uniform(0, background_height - traffic_cone_height))
        while x in range(crane_x, crane_x+crane_width) and y in range(crane_y, crane_y+crane_height):
            x = int(random.uniform(0, background_width - traffic_cone_width))
            y = int(random.uniform(0, background_height - traffic_cone_height))
        
        background_image.paste(traffic_cone_image,box=(x, y),mask=traffic_cone_image)
        
        annotation_content = {
            'segmentation': [],
            'area': traffic_cone_height * traffic_cone_width,
            'iscrowd': 0,
            'image_id': i,
            'bbox': [x, y, traffic_cone_width, traffic_cone_height],
            'category_id': 0,
            'id': j,
            'ignore': 0,
        }

        empty_json['annotations'].append(annotation_content)

    background_image.save(path + f'{i:>05}.jpg')
        


category_content = {
    "supercategory": "none",
    "id": 1,
    "name": 'crane'}
empty_json['categories'].append(category_content)
category_content = {
    "supercategory": "none",
    "id": 0,
    "name": 'traffic_cone'}
empty_json['categories'].append(category_content)

with open(path + '0.json', 'w') as outfile:
    json.dump(empty_json, outfile, indent = 2, ensure_ascii = False)