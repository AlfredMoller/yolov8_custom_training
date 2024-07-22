import os
import glob


def delete_xml_files(directory):
    # Encontrar todos los archivos .xml en el directorio especificado
    xml_files = glob.glob(os.path.join(directory, "*.xml"))

    # Eliminar cada archivo .xml encontrado
    for xml_file in xml_files:
        try:
            os.remove(xml_file)
            print(f"Eliminado: {xml_file}")
        except OSError as e:
            print(f"Error al eliminar {xml_file}: {e}")


# Ruta al directorio que contiene los archivos .xml
directory = 'images'

delete_xml_files(directory)
