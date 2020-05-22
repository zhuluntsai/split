from PIL import Image, ImageDraw, ImageFont
import os, shutil, json

all_json = json.load(open("0.json", "r"))
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30, encoding= 'utf-8')
color = (255, 0, 0)

for item in os.listdir():
    if item.endswith('jpg'):
        print(item)
        
        image = Image.open(item)
        image = image.convert('RGB')

        draw = ImageDraw.Draw(image)

        for annotations in all_json['annotations']:
            if annotations['image_id'] + ".jpg" == item:
                text_position = (annotations['bbox'][0], annotations['bbox'][1])
                rectangle_position = (annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3])
                
                draw.rectangle(rectangle_position, outline= color, width= 5)
                draw.text(text_position, annotations['id'], font= font, fill= color)

        image.save(item)
                