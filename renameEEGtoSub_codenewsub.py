import os
import pandas as pd

# Ruta base donde se encuentran las carpetas
base_path = '/bcbl/data/MRI/BIN/DATA/BIDS/raw/eeg'

# Nombres de las carpetas para cada grupo
folders = {'Group1': 'Group1', 'Group2': 'Group2', 'Group3': 'Group3'}

# Leer las correspondencias de nombres del archivo CSV
eeg_matches = pd.read_csv('/bcbl/data/MRI/BIN/DATA/BIDS/DABIDS/eeg_matches.csv')

sub_gen = (i for i in range(39, 239))  # Generador para sub identificadores
sub_dict = {}  # Diccionario global para rastrear los sub identificadores asignados

# Función para buscar y renombrar los archivos y actualizar el DataFrame
def rename_files(base_path, folders, matches):
    for index, row in matches.iterrows():
        original_name = row['original_name'].strip()
        new_name = row['new_name'].strip()

        if new_name == "NO MATCH FOUND":
            parts = original_name.split('_')
            if len(parts) > 2:
                subject_code = '_'.join(parts[:2])
            else:
                subject_code = parts[0]  # Fallback si hay menos de dos guiones bajos

            if subject_code not in sub_dict:
                sub_dict[subject_code] = next(sub_gen)
            sub_counter = sub_dict[subject_code]
            task_parts = parts[2:]  # Capturar el resto del nombre después del segundo guión bajo
            task_name = '_'.join(task_parts).strip()
            new_name = f"sub{sub_counter}_{task_name}"
            matches.at[index, 'new_name'] = new_name  # Actualizar el DataFrame con el nuevo nombre
            print(f"Assigned new name {new_name} for file {original_name}")

        group_identifier = original_name.split('_')[1]
        group_folder = folders.get(f'Group{group_identifier[-1]}')
        if not group_folder:
            print(f'No group found for file: {original_name}')
            continue
        
        search_path = os.path.join(base_path, group_folder)
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if original_name in file:
                    old_file_path = os.path.join(root, file)
                    new_file_path = os.path.join(root, file.replace(original_name.split('_')[0] + '_' + original_name.split('_')[1], f"sub{sub_counter}"))
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed {old_file_path} to {new_file_path}')
                    break

# Función para actualizar el CSV con los nuevos nombres
def update_csv(matches):
    matches.to_csv('/bcbl/data/MRI/BIN/DATA/BIDS/DABIDS/eeg_matches_updated.csv', index=False)
    print("CSV updated with new names.")

# Llamar a la función de renombramiento y luego actualizar el CSV
rename_files(base_path, folders, eeg_matches)
update_csv(eeg_matches)
