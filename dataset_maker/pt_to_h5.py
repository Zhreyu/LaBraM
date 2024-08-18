import os
import mne
import numpy as np
from pathlib import Path
from shock.utils.h5 import h5Dataset
import torch

def get_channel_order(ch_names):
    """
    Return the channel order from the EDF file channel names.
    """
    return ch_names

def process_edf_file(filepath):
    """
    Load an EDF file and return its data along with the number of channels and channel names.
    """
    raw = mne.io.read_raw_edf(filepath, preload=True)
    
    # Get the data and the channel information
    data = raw.get_data()  # shape will be (n_channels, n_times)
    channels = data.shape[0]
    ch_names = raw.ch_names
    
    return data, channels, ch_names

def save_to_h5(data_list, channels, save_dir):
    """
    Save the data into an HDF5 file grouped by the number of channels.
    """
    h5_filename = f"EEG_{channels}_channels"
    dataset = h5Dataset(Path(save_dir), h5_filename)
    
    for i, (filename, data, ch_names) in enumerate(data_list):
        grp = dataset.addGroup(grpName=Path(filename).stem)
        chunks = (channels, 500)  # Set chunks based on channels and data length
        dset = dataset.addDataset(grp, 'eeg', data, chunks)
        
        # Add relevant attributes
        dataset.addAttributes(dset, 'Channels', channels)
        dataset.addAttributes(dset, 'Timepoints', data.shape[1])
        
        # Set channel order based on the EDF file's channel names
        chOrder = get_channel_order(ch_names)
        dataset.addAttributes(dset, 'chOrder', chOrder)
    
    dataset.save()
    print(f"Saved HDF5 file: {h5_filename} with {channels} channels")

def main(raw_data_path, save_dir):
    """
    Main function to process EDF files and save them into HDF5 files grouped by the number of channels.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    channel_groups = {}

    # Iterate through all EDF files in the raw data directory
    for edf_file in os.listdir(raw_data_path):
        if edf_file.endswith('.edf'):
            filepath = os.path.join(raw_data_path, edf_file)
            data, channels, ch_names = process_edf_file(filepath)
            
            # Group data by the number of channels
            if channels not in channel_groups:
                channel_groups[channels] = []
            
            channel_groups[channels].append((edf_file, data, ch_names))
    
    # Save each group of data with the same number of channels into separate HDF5 files
    for channels, data_list in channel_groups.items():
        save_to_h5(data_list, channels, save_dir)

if __name__ == "__main__":
    raw_data_path = "C:\\Users\\shreyas\\Documents\\GitHub\\IEEG\\aaoutut\\"  # Replace with the path to your EDF files
    save_dir = "new_h5_dataset"       # Replace with the path where HDF5 files should be saved

    main(raw_data_path, save_dir)
