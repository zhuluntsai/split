import json

all_json = json.load(open("0.json", "r"))

amount_list = []

for categories in all_json['categories']:
    amount_list.append(0)

for annotations in all_json['annotations']:
    print(amount_list)
    amount_list[annotations['category_id'] - 1] += 1
total = 0
for categories in all_json['categories']:
    print(f"{categories['name']} : {amount_list[categories['id'] - 1]}")
    total += amount_list[categories['id'] - 1]

print(total)