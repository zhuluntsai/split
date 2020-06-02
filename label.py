from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, shutil, json

all_json = json.load(open("0.json", "r"))
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30, encoding= 'utf-8')
color = (255, 0, 0)

for item in os.listdir():
    if item.endswith('jpg'):
        print(item)
        
        image = Image.open(item)

        back = Image.new('RGBA', image.size)
        back.paste(image)
        
        poly = Image.new('RGBA', image.size)
        draw = ImageDraw.Draw(poly)

        for annotations in all_json['annotations']:
            if f"{annotations['image_id']:>05}.jpg" == item:
                text_position = (annotations['bbox'][0], annotations['bbox'][1])
                rectangle_position = (annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3])
                
                draw.polygon(annotations['segmentation'][0], fill=(255, 0, 0, 60), outline="blue")
                draw.rectangle(rectangle_position, outline= color, width= 6)
                draw.text(text_position, annotations['id'], font= font, fill= (255, 255, 255))

        back.paste(poly, (0,0), mask=poly)
        back.save(item, 'png')
                