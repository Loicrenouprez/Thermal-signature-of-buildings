# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:57:38 2023

@author: Loïc
"""

import numpy as np
import csv
import matplotlib.pyplot as plt


def nb_lines(file_path):
    file = open(file_path, 'r')
    csv_reader = csv.reader(file)
    line_count = sum(1 for row in csv_reader)
    file.close()
    return line_count

def treat_data(file_path, line_count):
   
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
    hour = 0
    for i in range(1, line_count):
        if i == 1 :
            a += float(rows[i][2].replace(',', '.'))
            nb_measure += 1
            continue
        if (int(rows[i][0][9:11])) != int((rows[i-1][0][9:11])) :
            #to handle the case of missing hours
            if abs((int(rows[i][0][9:11])) - int((rows[i-1][0][9:11]))) > 1 :
                nb_missing = (int(rows[i][0][9:11])) - int((rows[i-1][0][9:11]))
                for j in range(nb_missing) :
                    data[hour] = float(rows[i-1][2].replace(',', '.'))
                    hour += 1                       
            data[hour] = a/nb_measure
            nb_measure = 1
            a = 0.0
            hour += 1
        else :
            a += float(rows[i][2].replace(',', '.'))
            nb_measure += 1
        if i == (line_count-1):
            data[hour] = a/nb_measure
    file.close()
    return data

def treat_weather_data(file_path, nb_lines):
    file = open(file_path, 'r')
    csv_reader = csv.reader(file, delimiter =';')

    temp_array = []
    i = 0
    j = 0
    for row in csv_reader:
        #to avoid having the title of the column in the array
        if i == 0 :
            i +=1
            j = 0
            continue
        if len(row) > 4:
            temperature = row[4]
            temp_array.append(temperature)
            temp_array[j] = float(temp_array[j])
        j+=1

    return temp_array

def create_figure(heat_data, temperature_data):
    plt.scatter(temperature_data, heat_data, marker = 'o')
    min_temp = np.min(temperature_data)
    max_temp = np.max(temperature_data)
    print(int((max_temp-(-min_temp))/10))
    new_x_ticks = np.linspace(min_temp, max_temp, num = 10)
    print(new_x_ticks)
    plt.xticks(new_x_ticks)
    print(1)
    plt.xlabel('Temperature')
    plt.ylabel('Power supply [kW]')
    return 

if __name__ == "__main__":
    file_path1 = "donnes_chaleur/B67_CHA_RC_ECS.csv"
    file_path2 = "Weather_data_Solcast.csv"
    nb_lines = nb_lines(file_path1)
    heat_data = treat_data(file_path1, nb_lines)
    temperature_data = treat_weather_data(file_path2, 8761)
    create_figure(heat_data, temperature_data)
