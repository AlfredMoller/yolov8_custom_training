import os
import xml.etree.ElementTree as ET
from glob import glob


def convert_voc_to_yolo(voc_dir, yolo_dir, classes_file):
    # Leer las clases desde el archivo de clases y convertir a minúsculas
    with open(classes_file) as f:
        classes = [line.strip().lower() for line in f]
    print(f"Clases: {classes}")

    # Crear directorio de salida si no existe
    if not os.path.exists(yolo_dir):
        os.makedirs(yolo_dir)

    # Procesar cada archivo XML en el directorio VOC
    for xml_file in glob(os.path.join(voc_dir, "*.xml")):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        image_id = root.find("filename").text.replace(".jpg", "")
        width = int(root.find("size/width").text)
        height = int(root.find("size/height").text)

        print(f"Procesando {image_id}, width: {width}, height: {height}")

        # Crear el archivo YOLO
        yolo_file = os.path.join(yolo_dir, f"{image_id}.txt")
        with open(yolo_file, "w") as yolo_f:
            for obj in root.iter("object"):
                cls = obj.find("name").text.strip().lower()
                print(f"Clase encontrada en XML: '{cls}'")
                if cls not in classes:
                    print(f"Clase '{cls}' no encontrada en classes.txt")
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find("bndbox")
                xmin = float(xmlbox.find("xmin").text)
                ymin = float(xmlbox.find("ymin").text)
                xmax = float(xmlbox.find("xmax").text)
                ymax = float(xmlbox.find("ymax").text)

                # Calcular coordenadas YOLO normalizadas
                x_center = (xmin + xmax) / 2.0 / width
                y_center = (ymin + ymax) / 2.0 / height
                box_width = (xmax - xmin) / width
                box_height = (ymax - ymin) / height

                yolo_f.write(f"{cls_id} {x_center} {y_center} {box_width} {box_height}\n")
                print(f"Escribiendo: {cls_id} {x_center} {y_center} {box_width} {box_height}")


# Ruta al directorio de los archivos PascalVOC XML
voc_dir = 'images'
# Ruta al directorio donde se guardarán los archivos YOLO
yolo_dir = 'labels'
# Ruta al archivo de clases
classes_file = 'classes.txt'

convert_voc_to_yolo(voc_dir, yolo_dir, classes_file)
