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


def treat_data(file_path, line_count, time):

    file = open(file_path, 'r')
    csv_reader = csv.reader(file, delimiter=';')
    rows = []
    for row in csv_reader:
        cell_array = []
        for cell in row:
            cell_array.append(cell)
        rows.append(cell_array)

    nb_measure = 0
    data = []
    power = 0.0
    index_missing = []

    if time == 1:
        for i in range(1, line_count):
            if i == 1:
                power += float(rows[i][2].replace(',', '.'))
                nb_measure += 1
                continue
            if (int(rows[i][0][0:2])) != int((rows[i-1][0][0:2])):
                data.append(power/nb_measure)
                nb_measure = 1
                power = 0.0
            else:
                power += float(rows[i][2].replace(',', '.'))
                nb_measure += 1
            if i == (line_count-1):
                data.append(power/nb_measure)

    if time == 0:
        hour = 0
        for i in range(1, line_count):
            if i == 1:
                power += float(rows[i][2].replace(',', '.'))
                nb_measure += 1
                continue
            hour2 = int(rows[i][0][9:11])
            hour1 = int(rows[i-1][0][9:11])
            date2 = int(rows[i][0][0:2])
            date1 = int(rows[i-1][0][0:2])
            if hour2 != hour1 or date1 != date2:
                # to handle the case of missing hours
                if abs(hour2 - hour1) > 1 or date1 != date2:
                    if hour1 == 23 and hour2 == 0:
                        a = 0
                    else:
                        if date1 != date2 and hour1 == hour2:
                            if i == 177446:
                                print(int(rows[i][0][0:2]))
                                print(abs(hour2 - hour1))
                                print(hour2)
                                print(date2)
                                print(hour1)
                                print(date1)
                                print(hour)
                            date_changed = 1
                            hour, index_missing = compute_missing_hours(index_missing, hour2, hour1, hour, date_changed)
                        else :
                            date_changed = 0
                            hour, index_missing = compute_missing_hours(index_missing, hour2, hour1, hour, date_changed)
                            
                data.append(power/nb_measure)
                nb_measure = 1
                power = 0.0
                hour += 1
            else:
                power += float(rows[i][2].replace(',', '.'))
                nb_measure += 1
            if i == (line_count-1):
                data.append(power/nb_measure)
    file.close()
    return data, index_missing


def compute_missing_hours(index_missing, hour2, hour1, hour, date_changed):
    if date_changed == 1 :
        nb_missing = hour2-hour1 + 24
        print(nb_missing)
        print(hour)
        for j in range(nb_missing-1):
            index_missing.append(hour+j+1)
        hour += nb_missing-1
        
    else :
        if 1 <= hour2 <= 12 and 0 <= hour1 <= 12:
            nb_missing = hour2 - hour1
            for j in range(nb_missing-1):
                index_missing.append(hour+j+1)
            hour += nb_missing-1
    
        if 1 <= hour2 <= 12 and hour1 > 12:
            if hour1 > 12:
                nb_missing = (24-hour1) + hour2
                for j in range(nb_missing-1):
                    index_missing.append(hour+j+1)
            hour += nb_missing-1
    
        if 13 <= hour2 <= 23 and 0 <= hour1 <= 12:
            nb_missing = hour2 - hour1
            for j in range(nb_missing-1):
                index_missing.append(hour+j+1)
            hour += nb_missing-1
    
        if 13 <= hour2 <= 23 and 13 < hour1 <= 23:
            nb_missing = hour2 - hour1
            for j in range(nb_missing-1):
                index_missing.append(hour+j+1)
            hour += nb_missing-1
    
        if hour2 == 0:
            nb_missing = 24-hour1
            for j in range(nb_missing-1):
                index_missing.append(hour+j+1)
            hour += nb_missing-1
    # print('a')
    return hour, index_missing


# nb_lines = number of lines in the csv file
# time = the time scale you want to average your data : 0 = per hour and 1 = per day
# hour_missing = hours for which we have no information in the data of heat

def treat_weather_data(file_path, nb_lines, hour_missing, time):
    file = open(file_path, 'r')
    csv_reader = csv.reader(file, delimiter=';')

    rows = []
    for row in csv_reader:
        cell_array = []
        for cell in row:
            cell_array.append(cell)
        rows.append(cell_array)

    temp_array = []
    i = 0
    temp = 0
    nb_measure = 0
    if time == 1:
        for i in range(1, nb_lines):
            if i == 1:
                temp += float(rows[i][4])
                nb_measure += 1
                continue
            if (int(rows[i][2])) != (int(rows[i-1][2])):
                temp_array.append(temp/nb_measure)
                nb_measure = 1
                temp = 0.0
            else:
                temp += float(rows[i][4])
                nb_measure += 1
            if i == nb_lines-1:
                temp_array.append(temp/nb_measure)

    if time == 0:
        hour = 0
        j = 0
        for i in range(1, nb_lines):
            """"if i == 1:
                temp += float(rows[i][4])
                nb_measure += 1
                continue
            if (int(rows[i][3])) != (int(rows[i-1][3])):"""
            if hour == hour_missing[j]:
                if j < (np.shape(hour_missing)[0]-1):
                    j += 1
                else:
                    j = 0
                continue
            temp = float(rows[i][4])
            temp_array.append(temp)
            nb_measure = 1
            hour += 1
         
    file.close()
    return temp_array


def create_figure(heat_data, temperature_data):
    plt.scatter(temperature_data, heat_data, marker='o', s=10)
    min_temp = np.min(temperature_data)
    max_temp = np.max(temperature_data)
    new_x_ticks = np.linspace(min_temp, max_temp, num=10)
    plt.xticks(new_x_ticks)
    plt.xlabel('Temperature')
    plt.ylabel('Power supply [kW]')
    return


if __name__ == "__main__":
    file_path1 = "donnes_chaleur/B67_CHA_RC_ECS.csv"
    file_path2 = "Weather_data_Solcast.csv"
    nb_lines = nb_lines(file_path1)
    heat_data, hour_missing = treat_data(file_path1, nb_lines, 1)
    temperature_data = treat_weather_data(file_path2, 8761, hour_missing, 1)
    create_figure(heat_data, temperature_data)
