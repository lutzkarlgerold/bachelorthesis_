# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
from PIL import Image, ImageChops
import os

# Verzeichnis der Bilder
os.chdir("C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures/Gruppe1")

Probe = "004"
Datei1 = Probe+"-0-"
Datei2 = Probe+"-1-"
Datei3 = Probe+"-2-"

i=1

for x in range (0, 8):
    img_count = str(i)
    i = i+1 

    img1=Image.open(Datei1+img_count+".png")
    img2=Image.open(Datei2+img_count+".png")
    img3=Image.open(Datei3+img_count+".png")
    diff=ImageChops.difference(img1,img2)
    if diff.getbbox():
        diff.save("C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures/Gruppe1/diff/"+Datei2+img_count+"-diff.png")
    diff = ImageChops.difference(img1,img3)
    if diff.getbbox():
        diff.save(
            "C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures/Gruppe1/diff/"+Datei3+img_count+"-diff.png")

