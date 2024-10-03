import os
import shutil

# Definir los directorios raíz de los datos
mri_root = '/bcbl/data/MRI/BIN/DATA/BIDS/bidsfolder'
eeg_root = '/bcbl/data/MRI/BIN/DATA/BIDS/bidsfolder2'
output_root = '/bcbl/data/MRI/BIN/DATA/BIDS/bidsfoldermerged'


# Función para copiar archivos de MRI y EEG a la nueva estructura integrada
def integrate_data(mri_root, eeg_root, output_root):
    # Recorrer los sujetos de la carpeta EEG (porque todos tienen EEG)
    for root, dirs, files in os.walk(eeg_root):
        for dir_name in dirs:
            # Verificar si es un directorio de sujeto (sub-XX)
            if dir_name.startswith('sub-'):
                subject = dir_name
                
                # Crear la carpeta de sujeto en la nueva estructura
                subject_output_dir = os.path.join(output_root, subject)
                os.makedirs(subject_output_dir, exist_ok=True)
                
                # Recorrer las sesiones del sujeto
                for session in os.listdir(os.path.join(eeg_root, subject)):
                    session_dir = os.path.join(eeg_root, subject, session)
                    if os.path.isdir(session_dir) and session.startswith('ses-'):
                        
                        # Crear la carpeta de sesión en la nueva estructura
                        session_output_dir = os.path.join(subject_output_dir, session)
                        os.makedirs(session_output_dir, exist_ok=True)
                        
                        # Copiar la carpeta "eeg" a la nueva estructura
                        eeg_dir = os.path.join(session_dir, 'eeg')
                        if os.path.exists(eeg_dir):
                            shutil.copytree(eeg_dir, os.path.join(session_output_dir, 'eeg'), dirs_exist_ok=True)
                        
                        # Copiar todas las carpetas y archivos dentro de la sesión, excepto los archivos sub-XX_ses-Y_scans.tsv
                        mri_session_dir = os.path.join(mri_root, subject, session)
                        if os.path.exists(mri_session_dir):
                            for item in os.listdir(mri_session_dir):
                                item_path = os.path.join(mri_session_dir, item)
                                
                                # Ignorar archivos sub-XX_ses-Y_scans.tsv
                                if item.endswith('_scans.tsv'):
                                    continue
                                
                                if os.path.isdir(item_path):
                                    # Copiar carpetas (anat, dwi, fmap, func, etc.)
                                    shutil.copytree(item_path, os.path.join(session_output_dir, item), dirs_exist_ok=True)
                                else:
                                    # Copiar todos los demás archivos independientemente de la extensión
                                    shutil.copy2(item_path, session_output_dir)
                            
                            print(f'Integración completada para {subject} - {session} (MRI + EEG)')
                        else:
                            print(f'Integración completada para {subject} - {session} (solo EEG)')
                    else:
                        print(f'Sesión {session} no encontrada para {subject}')

# Ejecutar la integración
integrate_data(mri_root, eeg_root, output_root)
