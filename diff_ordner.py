# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
from PIL import Image, ImageChops
import os

# Verzeichnis der Bilder

def difference(Probe="004"):
    bild_format = "{}-{}-"

    Datei1 = bild_format.format(Probe, 0)
    Datei2 = bild_format.format(Probe, 1)
    Datei3 = bild_format.format(Probe, 2)
    Datei4 = bild_format.format(Probe, 3)
    Datei5 = bild_format.format(Probe, 4)
    Datei6 = bild_format.format(Probe, 5)
    Datei7 = bild_format.format(Probe, 6)
    Datei8 = bild_format.format(Probe, 7)
    Datei9 = bild_format.format(Probe, 8)


    i = 1

    for x in range(0, 8):
        img_count = str(i)
        i = i + 1

        img1 = Image.open(Datei1 + img_count + ".png")
        img2 = Image.open(Datei2 + img_count + ".png")
        img3 = Image.open(Datei3 + img_count + ".png")
        img4 = Image.open(Datei4 + img_count + ".png")
        img5 = Image.open(Datei5 + img_count + ".png")
        img6 = Image.open(Datei6 + img_count + ".png")
        img7 = Image.open(Datei7 + img_count + ".png")
        img8 = Image.open(Datei8 + img_count + ".png")
        img9 = Image.open(Datei9 + img_count + ".png")
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            diff.save("./diff/" + Datei2 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img3)
        if diff.getbbox():
            diff.save("./diff/" + Datei3 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img4)
        if diff.getbbox():
            diff.save("./diff/" + Datei4 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img5)
        if diff.getbbox():
            diff.save("./diff/" + Datei5 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img6)
        if diff.getbbox():
            diff.save("./diff/" + Datei6 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img7)
        if diff.getbbox():
            diff.save("./diff/" + Datei7 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img8)
        if diff.getbbox():
            diff.save("./diff/" + Datei8 + img_count + "-diff.png")
        diff = ImageChops.difference(img1, img9)
        if diff.getbbox():
            diff.save("./diff/" + Datei9 + img_count + "-diff.png")

if __name__ == '__main__':

    workdir = "C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures/Gruppe1"
    os.chdir(workdir)

    # difference("005")
    min_number = 1
    max_number = 150
    workdir_path = pathlib.Path(workdir)
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
