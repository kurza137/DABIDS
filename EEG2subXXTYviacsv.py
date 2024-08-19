from mne_bids.copyfiles import copyfile_brainvision
import pandas as pd
import os
import re  # Import necesario para usar re.match y re.sub

# Cargar los datos desde el CSV
csv_path = 'eeg_matches_updated.csv'
rename_data = pd.read_csv(csv_path)

# Limpiar los espacios adicionales en las columnas
rename_data['original_name'] = rename_data['original_name'].str.strip()

# Función para ajustar el nombre si es necesario
def adjust_name(name):
    # Extraer el número de subXX, por ejemplo, sub61
    match = re.match(r"sub(\d+)_", name)
    if match:
        # Convertir el número a entero
        num = int(match.group(1))
        # Si el número es 61 o mayor, restar uno
        if num >= 61:
            new_num = num - 1
            # Reemplazar el número en el nombre
            return re.sub(r"sub\d+", f"sub{new_num}", name, 1)
    return name

# Bucle para renombrar cada archivo según el CSV
for index, row in rename_data.iterrows():
    adjusted_name = adjust_name(row['new_name'])
    original_path = '/bcbl/data/MRI/BIN/DATA/BIDS/EEG/' + row['original_name']
    new_path = '/bcbl/data/MRI/BIN/DATA/BIDS/EEG/renamed/' + adjusted_name

    # Verificar si el archivo original existe y si la extensión es correcta
    if os.path.exists(original_path) and original_path.endswith('.vhdr'):
        try:
            copyfile_brainvision(original_path, new_path, verbose=True)
        except Exception as e:
            print(f"Error al copiar {original_path} a {new_path}: {e}")
    else:
        print(f"El archivo {original_path} no existe o la extensión no es .vhdr")
