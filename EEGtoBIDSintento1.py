import os
import re
import mne
from mne_bids import write_raw_bids, BIDSPath, print_dir_tree

# Directorio raíz de tus datos en formato BrainVision
data_root = '/bcbl/data/MRI/BIN/DATA/BIDS/chopped/EEG'
# Directorio raíz BIDS
bids_root = '/bcbl/data/MRI/BIN/DATA/BIDS/bidsfolder2'

# Función para extraer información del nombre del archivo
def parse_filename(filename):
    match = re.match(r'(sub)(\d+)_T(\d+)_(\w+)', filename)
    if match:
        prefix, subject, session, task = match.groups()
        return subject, session, task
    return None, None, None

def process_and_convert_to_bids(data_root, bids_root):
    for root, dirs, files in os.walk(data_root):
        for file in files:
            if file.endswith('.vhdr'):
                subject, session, task = parse_filename(file)
                if subject and session and task:
                    try:
                        # Cargar los datos
                        raw = mne.io.read_raw_brainvision(os.path.join(root, file), preload=False)
                        raw.info["line_freq"] = 50  # Ajusta esto según tu configuración específica

                        # Crear el objeto BIDSPath
                        bids_path = BIDSPath(subject=subject, session=session, task=task, root=bids_root)

                        # Convertir a BIDS
                        write_raw_bids(raw, bids_path, overwrite=True)
                        print(f'Converted {file} to BIDS format.')
                    except Exception as e:
                        print(f'Error processing {file}: {e}')
                else:
                    print(f'Ignored {file} due to unexpected filename format')


# Procesar y convertir todos los archivos .vhdr a BIDS
process_and_convert_to_bids(data_root, bids_root)


