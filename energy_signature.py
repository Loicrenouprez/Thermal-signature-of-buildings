# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:57:38 2023

@author: Loïc
"""

import numpy as np
import csv

file_path = "donnes_chaleur/B67_CHA_RC_ECS.csv"

file = open(file_path, 'r')
csv_reader = csv.reader(file)

line_count = sum(1 for row in csv_reader)
file.close()
file = open(file_path, 'r')
csv_reader = csv.reader(file, delimiter =';')
rows = []
for row in csv_reader:
    cell_array = []
    for cell in row:
        cell_array.append(cell)  
    rows.append(cell_array)

  
nb_measure = 0
data = np.zeros((8760), dtype = float)

a = 0.0
date = 0
for i in range(1, 578):
    if i == 1 :
        a += float(rows[i][2].replace(',', '.'))
        nb_measure += 1
        continue
    if (rows[i][0][8:10]) != (rows[i-1][0][8:10]) :
        print(i)
        data[date] = (a)/(nb_measure)
        nb_measure = 0
        a = 0.0
        date += 1
    else :
        a += float(rows[i][2].replace(',', '.'))
        nb_measure += 1
    if i == (line_count-1):
        data[date] = a/nb_measure

print(data)

