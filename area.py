import matplotlib.pyplot as plt 
import json
import numpy as np

all_json = json.load(open("0.json", "r"))
ratio = []
n = []
i = 0

for images in all_json['images']:
    all_area = images['height'] * images['width']

    for annotations in all_json['annotations']:
        
        if str(annotations['image_id']) == f"temp_{str(images['id']):>05}":
            # if annotations['area'] / all_area <= 1:
            i += 1
            # ratio.append(annotations['area'] / all_area)
            ratio.append(annotations["area"] / (annotations["bbox"][2] * annotations["bbox"][3]))
            n.append(i)
            
            continue


fig = plt.figure(1) 
# plt.plot(n, ratio, 'bo') 
plt.hist(ratio, bins= np.array(range(0, 101, 1)) * 0.01)
plt.xlabel('image id', fontsize=20) 
plt.ylabel('area filter ratio', fontsize=20) 
plt.grid(True)

plt.show()
# plt.savefig('area.png',dpi=300) 
plt.close(fig)