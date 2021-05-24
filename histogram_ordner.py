# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:30:54 2021

@author: lg
"""
import numpy as np
import cv2
import csv
import glob, os
from scipy import stats

# Verzeichnis der Bilder
os.chdir("C:/Users/lg/Dokumente/BA/bachelorthesis/input_pictures") = Folder

# Anzahl der png-Dateien im Ordner zählen
#Folder = "C:\\"
Counter = 0
Files = os.listdir(Folder)

for File in Files:
    [Dummy, Ext] = os.path.splitext(File)
    if Ext == ".png":
        Counter += 1

# Ort der Liste mit Noten
# grades = ("C:/Users/lg/Dokumente/BA/bachelorthesis/Notenliste/grades.txt")

# Ort der Outputdaten
# output = ("C:/Users/lg/Dokumente/BA/004-013 Erste Serie für NN/Test 5 Histowerte via Py/output_dir")

# Output-Noten als Dictionary einlesen
with  open("C:/Users/lg/Dokumente/BA/bachelorthesis/Notenliste/grades.txt", "r") as f:
    rows = ( line.rstrip('\n').split('\t') for line in f )
    d = { row[0]:row[1] for row in rows }
    print(d)

# Header des Daten-Files erstellen        
with open('input_daten.txt', 'a', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=' ')
    csv_output.writerow(Counter)

# Header des Noten-Files erstellen
with open('input_noten.txt', 'a', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=' ')
    csv_output.writerow(['Note'])
    
for file in glob.glob("*.png"):
    print (os.path.basename(file))
    sample = os.path.basename(file)
    file[0]
    samplename = file[0]+file[1]+file[2]+file[3]+file[4]
#    print (samplename)

    image0 = cv2.imread(file)

    hist = image0
    
    mode = stats.mode(hist)
    total_mode = stats.mode(hist, axis=None)

    # Histogramm-Daten in TXT-file schreiben    
    with open('input_daten.txt', 'a', newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter=' ')
        csv_output.writerow([int(np.mean(hist)), int(np.std(hist)), np.max(hist), format(total_mode.mode[0])])
    print ("Mean = {:.1f}, standard deviation = {:.1f}, Count = {:.0f}, min = {:.0f}, max = {:.0f}".format(
        np.mean(hist).item(),
        np.std(hist).item(),
        len(hist)*len(hist),
        np.min(hist).item(),
        np.max(hist).item()
        ))

    print("mode = {}".format(total_mode.mode[0]))
    
    # Noten aus Dictionary in TXT-File schreiben
    dict = d
    sn = dict.get(samplename)
#    float(sn)
    print ("Note: %s" % sn)

    with open('input_noten.txt', 'a', newline='') as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerow([sn])       
        
cv2.waitKey(0)