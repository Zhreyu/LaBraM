import h5py
import os

def verify_h5_file(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            # Check if the file contains any groups or datasets
            if len(f.keys()) == 0:
                print(f"File {file_path} is empty.")
                return False
            
            # Iterate through each group
            for group_name in f.keys():
                group = f[group_name]
                
                # Ensure it's a group, not just a dataset
                if isinstance(group, h5py.Group):
                    # Iterate through each dataset in the group
                    for dataset_name in group.keys():
                        dataset = group[dataset_name]
                        
                        # Check if the dataset is empty
                        if dataset.size == 0:
                            print(f"Dataset {dataset_name} in group {group_name} of file {file_path} is empty.")
                            return False
                        
                        # Check for any obvious corruption by attempting to read the dataset
                        try:
                            data = dataset[()]
                        except Exception as e:
                            print(f"Failed to read dataset {dataset_name} in group {group_name} of file {file_path}. Error: {e}")
                            return False
                else:
                    # Handle case where a key in the root level is a dataset directly
                    dataset = group
                    if dataset.size == 0:
                        print(f"Dataset {group_name} in file {file_path} is empty.")
                        return False
                    
                    try:
                        data = dataset[()]
                    except Exception as e:
                        print(f"Failed to read dataset {group_name} in file {file_path}. Error: {e}")
                        return False

        print(f"File {file_path} is valid.")
        return True

    except Exception as e:
        print(f"Error opening file {file_path}. Error: {e}")
        return False

def verify_h5_files(directory):
    # Iterate over all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".hdf5") or file.endswith(".h5"):
                file_path = os.path.join(root, file)
                verify_h5_file(file_path)

# Usage example
directory_path = 'new_h5_dataset'  # Update this to your HDF5 directory
verify_h5_files(directory_path)
