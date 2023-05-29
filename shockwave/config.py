import os
import sys
import csv

def load():
    '''
    file = open("configure.csv", "r")
    data = list(csv.reader(file, delimiter=","))
    file.close()
    return data[0], data[1:] 
    '''
    config_items = []
    # Open the CSV file 
    with open('configure.csv', 'r') as file:
        # Create a DictReader object
        reader = csv.DictReader(file)
        for row in reader:
            converted_row = {key: int(value) if key != 'image_foldername' else value for key, value in row.items()}
            config_items.append(converted_row)
        file.close()
    return config_items
#item_names, config_items = load()
