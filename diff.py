# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:19:25 2020

@author: lg
"""
#from PIL import Image, ImageChops
from PIL import Image, ImageChops

Datei1 = "013-0-Muster10-"
Datei2 = "013-2-Muster10-"

i=0

for x in range (0, 8):
    img_count = str(i)
    i = i+1 

    img1=Image.open(Datei1+"0.png")
    img2=Image.open(Datei2+img_count+".png")
    diff=ImageChops.difference(img1,img2)
    if diff.getbbox():
        diff.save("C:/Users/lg/Dokumente/BA/004-129 finale Serie für NN/Diff_0_vs_alle/"+Datei2+img_count+"-diff.png")