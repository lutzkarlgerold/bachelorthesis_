# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
import pathlib
from PIL import Image, ImageChops
import os
import datetime

# Verzeichnis der Bilder

def difference(Probe="004", n_images_max=2):
    bild_format = "{}-{}-"
    bilder = []
    
    for i in range(9):
        try:
            bilder.append(bild_format.format(Probe, n_images_max +1))
        except FileNotFoundError as F_e:
            if i == 0:
                raise F_e
            else:
                print(f"found {i+1} images for {Probe}")
                break
    print(f"found {i+1} images for {Probe}")
    i = 1

    for x in range(0, 8):
        img_count = str(i)
        i = i + 1
        images = []
        for i_p in bilder:
            images.append(Image.open(i_p + img_count + ".png"))

        for i, image in enumerate(images[1:]):
            diff = ImageChops.difference(images[0], image)

            if diff.getbbox(): # hier ist irgendwas falsch
                print(1)
                diff.save("./diff/" + bilder[i+1] + img_count + "-diff.png")

if __name__ == '__main__':

    workdir = "./input_pictures/Gruppe1"
    os.chdir(workdir)

    # difference("005")
    min_number = 1
    max_number = 150
    workdir_path = pathlib.Path(".")
    print(workdir_path.iterdir())
    path_content = [x for x in workdir_path.iterdir()]
    number_format = "{:03}"

    for i_p in range(min_number, max_number):
        try:
            difference(number_format.format(i_p))
            print(f"Probe {i_p} bearbeitet um: {datetime.datetime.now()}")
        except FileNotFoundError:
            print(f"Probe {i_p} existiert nicht ")

    print(number_format.format(max_number))
    print(number_format.format(min_number))
