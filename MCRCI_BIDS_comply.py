# This is an ad-hoc script to make the MCRCI project output BIDS-compatible. It first checks for the presence of the numerical pattern and then maps this number to a corresponding subject number,
# which is sequentially incremented each time a new original number is found.
# It then proceeds to rename the folders according to the new name format you have specified.

# It also saves a record in participants_log.csv, which you can use later to add the relevant data to the participants.tsv file.

import os
import re
import csv

def rename_folders_and_create_log(source_dir, log_path):
    # Contador para las carpetas renombradas
    renamed_folders_count = 0
    
    # Mapa para llevar el seguimiento de los números de sujetos asignados
    subject_number_map = {}
    next_subject_number = 1
    
    # Diccionario para mapear MCRCI a estados de participantes
    mcrci_to_state = {
        "1": "patient_new",
        "2": "patient_treated",
        "3": "control"
    }
    
    # Lista para guardar la información de los participantes
    participants_info = []
    
    # Set para almacenar combinaciones únicas de número original y secuencia MCRCI
    unique_combinations = set()

    # Recorrer el directorio fuente
    for folder_name in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, folder_name)):
            # Extraer el número al principio del nombre de la carpeta
            match = re.match(r"(\d+)_MCRCI(\d)_T(\d)", folder_name)
            if match:
                original_number = match.group(1)
                mcrci_sequence = match.group(2)
                time_point = match.group(3)
                unique_key = f"{original_number}_MCRCI{mcrci_sequence}"

                # Asignar un nuevo número de sujeto si aún no tiene uno
                if unique_key not in unique_combinations:
                    unique_combinations.add(unique_key)
                    subject_number_map[unique_key] = next_subject_number
                    next_subject_number += 1

                # Construir el nuevo nombre de la carpeta
                new_folder_name = f"sub{str(subject_number_map[unique_key]).zfill(2)}_T{time_point}"
                
                # Renombrar la carpeta
                original_path = os.path.join(source_dir, folder_name)
                new_path = os.path.join(source_dir, new_folder_name)
                
                if not os.path.exists(new_path):  # Asegurarse de que el nuevo path no exista
                    os.rename(original_path, new_path)
                    renamed_folders_count += 1
                    
                    # Guardar la información en la lista de participantes
                    participants_info.append({
                        "original_name": folder_name,
                        "new_name": new_folder_name,
                        "original_number": original_number,
                        "mcrci_sequence": mcrci_sequence,
                        "state": mcrci_to_state[mcrci_sequence],
                        "time_point": time_point
                    })
                    
                    print(f"Renamed: {folder_name} to {new_folder_name}")
                else:
                    print(f"Error: The path {new_path} already exists. Cannot rename {folder_name} to {new_folder_name}")
    
    # Escribir la información en el archivo de log
    with open(log_path, 'w', newline='') as file:
        fieldnames = ['original_name', 'new_name', 'original_number', 'mcrci_sequence', 'state', 'time_point']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in participants_info:
            writer.writerow(entry)
    
    print(f"Total folders renamed: {renamed_folders_count}")
    print(f"Participants information logged at: {log_path}")

if __name__ == "__main__":
    # Definir el directorio fuente y el archivo de log
    source_dir = "/bcbl/data/MRI/BIN/DATA/BIDS"
    log_path = "/bcbl/data/MRI/BIN/DATA/BIDS/participants_log.csv"
    rename_folders_and_create_log(source_dir, log_path)
