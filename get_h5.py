import os

folder_path = 'new_h5_dataset'
dataset_list = []
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        if file_name.endswith('.h5') or file_name.endswith('.hdf5'):
            dataset_list.append([os.path.join(folder_path, file_path)])
        
        
print(dataset_list)