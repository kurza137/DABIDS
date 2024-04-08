import os
import shutil

# Path to the directory containing the folders
# Asegúrate de cambiar 'your_directory_path' a la ruta de tu directorio
path = '/bcbl/data/MRI/BIN/DATA/BIDS'

# List all items in the directory
items = os.listdir(path)

# Initialize a dictionary to keep track of the main folders and their sub-sessions
main_folders = {}

# Process each item in the directory
for item in items:
    # Check if the item is a folder and matches the pattern "subXX_TX"
    if os.path.isdir(os.path.join(path, item)) and item.startswith('sub') and '_T' in item:
        # Extract the main folder name and session number
        main_folder, session = item.split('_T')
        session_number = int(session)

        # Add the main folder to the dictionary if not already present
        if main_folder not in main_folders:
            main_folders[main_folder] = {}

        # Create a subfolder "sesX" inside the main folder if it doesn't exist
        session_folder = f'ses{session_number}'
        session_path = os.path.join(path, main_folder, session_folder)
        os.makedirs(session_path, exist_ok=True)

        # Move contents of the original folder to the new subfolder
        original_path = os.path.join(path, item)
        for content in os.listdir(original_path):
            shutil.move(os.path.join(original_path, content), session_path)

        # Record the session subfolder in the main folder's dictionary
        main_folders[main_folder][session_folder] = session_path

# Clean up the directory by removing the now-empty original folders and rename if needed
for main_folder, sessions in main_folders.items():
    # Determine the new folder name without the "_TX" suffix
    new_folder_name = main_folder.split('_')[0]
    old_folder_path = os.path.join(path, main_folder)
    new_folder_path = os.path.join(path, new_folder_name)

    # Rename the main folder to remove "_T1" or "_T2"
    if os.path.exists(old_folder_path) and not os.path.exists(new_folder_path):
        os.rename(old_folder_path, new_folder_path)

    for session_folder, session_path in sessions.items():
        # Remove the original folder only if it is empty
        original_folder_path = os.path.join(path, f"{main_folder}_T{session_folder[-1]}")
        if not os.listdir(original_folder_path):
            os.rmdir(original_folder_path)

# The script does not output anything unless you add print statements
