# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
import pathlib
from PIL import Image, ImageChops
import os
import datetime

def ensure_directory(target_folder: [str, os.path], recursive=False) -> None:
    """
    generates directories if they do not exist recursively if desired
    :param target_folder:
    :param recursive:
    :return:
    """
    if recursive:
        subfolders = target_folder.split("/")
        for f_n in range(len(subfolders)):
            folder = "/".join(subfolders[:f_n + 1])
            if not os.path.exists(folder):
                try:
                    os.mkdir(folder)
                except OSError:
                    logging.error(f"failed to create folder {folder}")
    else:
        if not os.path.exists(target_folder):
            try:
                os.mkdir(target_folder)
            except OSError:
                logging.error(f"failed to create folder {target_folder}")
# Verzeichnis der Bilder

def difference(Probe="004", n_images_max=8):
    bild_format = "{}-{}-"
    bilder = []
    
    for i in range(n_images_max+1):

        bilder.append(bild_format.format(Probe, i))



    i = 1

    for x in range(0, 8):
        img_count = str(i)
        i = i + 1
        images = []
        first = True
        for image_name in bilder:

            try:
                images.append(Image.open(image_name + img_count + ".png"))
                first = False
            except FileNotFoundError as F_e:
                if first:
                    raise F_e
                else:
                    break
        for j, image in enumerate(images[1:]):
            diff = ImageChops.difference(images[0], image)

            if diff.getbbox():  # hier ist irgendwas falsch

                ensure_directory("./diff")
                print(bilder[j+1] + str(i) + "-diff.png")
                diff.save("./diff/" + bilder[j+1] + str(i) + "-diff.png")

if __name__ == '__main__':

    workdir = "./input_pictures/Gruppe1"
    os.chdir(workdir)

    # difference("005")
    min_number = 127
    max_number = 150
    workdir_path = pathlib.Path(".")
    print(workdir_path.iterdir())
    path_content = [x for x in workdir_path.iterdir()]
    number_format = "{:03}"

    for i_p in range(min_number, max_number):
        try:
            difference(number_format.format(i_p))
            print(f"Probe {i_p} bearbeitet um: {datetime.datetime.now()}")
        except FileNotFoundError as F_e:
            print(f"Probe {i_p} existiert nicht ")
            raise F_e
    print(number_format.format(max_number))
    print(number_format.format(min_number))
