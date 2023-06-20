import os
import sys
import csv

def load(config_file_path, non_integer_key_name):
    config_items = []
    # Open theconfig_file_path
    with open(config_file_path, 'r') as file:
        # Create a DictReader object
        reader = csv.DictReader(file)
        for row in reader:
            converted_row = {key: int(value) if key != non_integer_key_name else value for key, value in row.items()}
            config_items.append(converted_row)
        file.close()
    return config_items