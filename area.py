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
            # ratio.append(annotations["area"] / (annotations["bbox"][2] * annotations["bbox"][3]))
            ratio.append(annotations['area'] / all_area)
            # ratio.append((annotations["bbox"][2] * annotations["bbox"][3]) / all_area)
            n.append(i)
            
            continue

print(len(ratio))
fig = plt.figure(1) 
# plt.plot(n, ratio, 'bo') 
plt.hist(ratio, bins= np.array(range(0, 21, 1)) * 0.05)
# plt.xlabel('polygon area / bbox area', fontsize=16) 
plt.xlabel('polygon area / whole image area', fontsize=16)
plt.ylabel('annotation amount', fontsize=16) 
plt.grid(True)

# plt.show()
plt.savefig('area2_hist.png',dpi=300) 
plt.close(fig)