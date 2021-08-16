import os, shutil
from tqdm import tqdm

dataset_list = ['person', 'traffic_cone']
start_list = [40000, 20000]
aug_times_list = [0, 5]

version = '9.5'

destination_path = f'/home/user/Documents/weilun/all/v{version}/'

if os.path.exists(destination_path):
    shutil.rmtree(destination_path)
os.makedirs(destination_path)

for i, dataset in enumerate(dataset_list):
    for root, dirs, file in os.walk(os.getcwd()):
        if root.endswith(dataset):
            
            folder_name = root.split('/')[-1]
            print(f' copy from "{root}" to "{destination_path}"')

            for filename in file:
                shutil.copy(f'{root}/{filename}', f'{destination_path}/{filename}')

            cmd = f'python filename.py -f {destination_path}{folder_name}.json -s {start_list[i]} -i {destination_path}'
            os.system(cmd)

            cmd = f'python augmentation.py -f {destination_path}{folder_name}.json -n {aug_times_list[i]} -i {destination_path}'
            os.system(cmd)

shutil.copy(f'/home/user/Documents/weilun/dataset/split.py', f'{destination_path}split.py')
cmd = f'python {destination_path}split.py -i {destination_path} -f -s'
os.system(cmd)