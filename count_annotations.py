import json
import argparse

def create_parser():

    parser = argparse.ArgumentParser(formatter_class= argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--filename", type= str)
    arg = parser.parse_args()

    return arg

arg = create_parser()
all_json = json.load(open(arg.filename, "r"))

amount_list = []
total = 0

for categories in all_json['categories']:
    amount_list.append(0)
amount_list.append(0)

for annotations in all_json['annotations']:
    amount_list[annotations['category_id'] - 1] += 1
    
for categories in all_json['categories']:
    print(f"{amount_list[categories['id'] - 1]}\t <<<<<< {categories['name']}")
    total += amount_list[categories['id'] - 1]

print(f"\n{total}\t <<<<<< total\n")