import xmltodict
import json
import os
import argparse
import pathlib

parser = argparse.ArgumentParser(description = 'Crop object from image according to detection-tracking bbox')
parser.add_argument('--xml', default = '/Users/weiluntsai/Desktop/entire_dataset', type=str, help = 'xml directory to be convert')
parser.add_argument('--json', default = '/Users/weiluntsai/Desktop/entire_dataset', type=str, help = 'json directory to be saved')
args = parser.parse_args()

args.xml = str(pathlib.Path().absolute())
args.json = str(pathlib.Path().absolute())

def ConvertXMLtoJSON(xml_path, xml_name, json_path):
    xml_path = os.path.join(xml_path, xml_name)
    with open(xml_path) as in_file:
        xml = in_file.read()
        json_name = xml_name[len(xml_name) - 10 : len(xml_name) - 4]
        path = os.path.join(json_path, json_name + '.json')
        with open(path, 'w') as out_file:
            json.dump(xmltodict.parse(xml), out_file)

def main():
    xml_names = os.listdir(args.xml)
    xml_names.sort()
    for xml_name in xml_names:
        if xml_name[len(xml_name) - 4 :] == '.xml':
            ConvertXMLtoJSON(args.xml, xml_name, args.json)
            print('Succeed to convert', xml_name)

if __name__ == '__main__': 
	main()