"""
Skyler Heininger
CS 3050
This script will convert a csv into the json equivalent.
"""

import csv
import json


def load_csv(input_filepath):
    """
    This function will load a csv from the given file. This additionally cleans the script as necessary for
    firebase functionality
    :param input_filepath: String, location of the given file
    :return: A dictionary representation of the csv file
    """
    # Read the CSV file
    csv_data = {}
    with open(input_filepath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for index, row in enumerate(csv_reader, start=1):
            # Create a unique key based on the index or rank
            key = f"University{index}"

            # Exclude keys with empty names ("")
            new_row = {key.replace(char, '_'): value for key, value in row.items() if key != "" for char in
                       ['.', '#', '$', '[', ']', '/']}
            # Only add the row to the dictionary if it has non-empty keys
            if new_row:
                csv_data[key] = new_row
    return csv_data


def save_json(data_dictionary, output_filepath):
    """
    This data will save the data to a json, from the data in a dictionary
    :param data_dictionary: Dictionary, the data to save
    :param output_filepath: String, the name of the given file
    :return: None
    """
    # Save to Json
    with open(output_filepath, 'w') as json_file:
        json.dump(data_dictionary, json_file, indent=2)


if __name__ == "__main__":
    # Specify file paths
    csv_path = "top_100_uni_world_eq.csv"
    json_path = "top_100_uni_world_eq.json"

    # Load csv
    data = load_csv(csv_path)

    # Save to json
    save_json(data, json_path)
    print("Data conversion done, please ensure this worked by checking the file")

