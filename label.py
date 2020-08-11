from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, shutil, json, argparse

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter, description= '''\
 description:

    - program will visualize the labeling data
    
    - type -f to set the file name
    - type -r to draw rectangle
    - type -p to draw polygon
    - type -t to add annotation id on rectangle
    - type -font to set file path of font, ex: "/System/Library/Fonts/Supplemental/Arial.ttf"
    ''')

    parser.add_argument("-f", "--file_name", help= "json file name", type= str)
    parser.add_argument("-r", "--draw_rectangle", help= "draw rectangle", action = "store_true")
    parser.add_argument("-p", "--draw_polygon", help= "draw polygon", action = "store_true")
    parser.add_argument("-t", "--add_text", help= "add text", action = "store_true")
    parser.add_argument("-font", help= "set file path of font", type= str, default= "/System/Library/Fonts/Supplemental/Arial.ttf")

    arg = parser.parse_args()
    return arg

arg = create_parser()

all_json = json.load(open(arg.file_name, "r"))
font = ImageFont.truetype(arg.font, 30, encoding= 'utf-8')
color = (255, 0, 0)

for item in os.listdir():
    if item.endswith('.jpg'):
        print(item)
        
        image = Image.open(item)

        back = Image.new('RGBA', image.size)
        back.paste(image)
        
        poly = Image.new('RGBA', image.size)
        draw = ImageDraw.Draw(poly)

        for annotations in all_json['annotations']:
            if f"{annotations['image_id']:>05}.jpg" == item:
                text_position = (annotations['bbox'][0], annotations['bbox'][1])

                if len(annotations['bbox']) == 4:
                    rectangle_position = (annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][0] + annotations['bbox'][2], annotations['bbox'][1] + annotations['bbox'][3])
                else:
                    rectangle_position = (annotations['bbox'][0], annotations['bbox'][1], annotations['bbox'][2], annotations['bbox'][3])

                if arg.draw_rectangle == True:
                    draw.rectangle(rectangle_position, outline= color, width= 6)
                if arg.draw_polygon == True:
                    draw.polygon(annotations['segmentation'][0], fill=(255, 0, 0, 60), outline="blue")
                if arg.add_text == True:
                    for categories in all_json['categories']:
                        if categories['id'] == annotations['category_id']:
                            draw.text(text_position, categories['name'], font= font, fill= (255, 255, 255))

        back.paste(poly, (0,0), mask=poly)
        back.save(item, 'png')
                