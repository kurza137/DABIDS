# This is an ad-hoc script to make the MCRCI project output BIDS-compatible. It first checks for the presence of the numerical pattern and then maps this number to a corresponding subject number,
# which is sequentially incremented each time a new original number is found.
# It then proceeds to rename the folders according to the new name format you have specified.

# It also saves a record in participants_log.csv, which you can use later to add the relevant data to the participants.tsv file.

import os
import re
import csv

def rename_folders_and_create_log(source_dir, log_path):
    # Counter for renamed folders
    renamed_folders_count = 0
    
    # Map to track the assigned subject numbers
    subject_number_map = {}
    next_subject_number = 1
    
    # Dictionary to map MCRCI to participant states
    mcrci_to_state = {
        "1": "patient_new",
        "2": "patient_treated",
        "3": "control"
    }
    
    # List to save the information of the participants
    participants_info = []

    # Browse the source directory
    for folder_name in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, folder_name)):
            # Extract the number at the beginning of the folder name
            match = re.match(r"(\d+)_MCRCI(\d)_T(\d)", folder_name)
            if match:
                original_number = match.group(1)
                mcrci_sequence = match.group(2)
                time_point = match.group(3)

                # Assign a new subject number if it does not have one yet
                if original_number not in subject_number_map:
                    subject_number_map[original_number] = next_subject_number
                    next_subject_number += 1
                
                # Build the new folder name
                new_folder_name = f"sub{str(subject_number_map[original_number]).zfill(2)}_T{time_point}"
                
                # Rename the folder
                original_path = os.path.join(source_dir, folder_name)
                new_path = os.path.join(source_dir, new_folder_name)
                os.rename(original_path, new_path)
                renamed_folders_count += 1
                
                # Save the information in the participants list
                participants_info.append({
                    "original_name": folder_name,
                    "new_name": new_folder_name,
                    "original_number": original_number,
                    "mcrci_sequence": mcrci_sequence,
                    "state": mcrci_to_state[mcrci_sequence],
                    "time_point": time_point
                })
                
                print(f"Renamed: {folder_name} to {new_folder_name}")
    
    # Write the information in the log file
    with open(log_path, 'w', newline='') as file:
        fieldnames = ['original_name', 'new_name', 'original_number', 'mcrci_sequence', 'state', 'time_point']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in participants_info:
            writer.writerow(entry)
    
    print(f"Total folders renamed: {renamed_folders_count}")
    print(f"Participants information logged at: {log_path}")

if __name__ == "__main__":
    # Define the source directory and the log file
    source_dir = "/bcbl/data/MRI/BIN/DATA/BIDS"
    log_path = "/bcbl/data/MRI/BIN/DATA/BIDS/participants_log.csv"
    rename_folders_and_create_log(source_dir, log_path)
