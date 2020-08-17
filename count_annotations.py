import json

training_data_json = json.load(open("training_data.json", "r"))
testing_data_json = json.load(open("testing_data.json", "r"))

crane = 0
boom = 0

for annotations in training_data_json['annotations']:
    if annotations['category_id'] == 1:
        crane += 1
    elif annotations['category_id'] == 2:
        boom += 1

for annotations in testing_data_json['annotations']:
    if annotations['category_id'] == 1:
        crane += 1
    elif annotations['category_id'] == 2:
        boom += 1

print(crane)
print(boom)
print(crane + boom)