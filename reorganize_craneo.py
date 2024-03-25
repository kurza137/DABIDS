#BIDS requiere una organización específica de los datos RAW, en BCBL exportamos los DICOM a los distintos proyectos usando OsiriX. El primer paso es borrar la carpeta intermedia CRANEO_FUNCIONAL

import os
import shutil

def reorganize_craneo_functional(source_dir):
    # Contador para los archivos movidos
    moved_files_count = 0
    
    # Contador para las carpetas eliminadas
    removed_folders_count = 0
    
    # Recorrer el directorio fuente
    for root, dirs, files in os.walk(source_dir):
        for dir_name in dirs:
            # Construye el camino completo hacia la carpeta intermedia
            intermediate_dir_path = os.path.join(root, dir_name)
            # Verificar si la carpeta intermedia contiene 'CRANEO_FUNCIONAL'
            if "CRANEO_FUNCIONAL" in dir_name:
                # Mover cada archivo de la carpeta intermedia al directorio padre
                for file_name in os.listdir(intermediate_dir_path):
                    file_path = os.path.join(intermediate_dir_path, file_name)
                    new_path = os.path.join(root, file_name)
                    shutil.move(file_path, new_path)
                    moved_files_count += 1
                # Eliminar la carpeta intermedia vacía
                os.rmdir(intermediate_dir_path)
                removed_folders_count += 1
                print(f"Reorganized: {intermediate_dir_path}")
    
    print(f"Total files moved: {moved_files_count}")
    print(f"Total folders removed: {removed_folders_count}")

if __name__ == "__main__":
    # Definir el directorio fuente
    source_dir = "/bcbl/data/MRI/BIN/DATA/BIDS"
    reorganize_craneo_functional(source_dir)
