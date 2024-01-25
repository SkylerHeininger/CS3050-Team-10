"""
Skyler Heininger
CS 3050
This script will convert a csv into the json equivalent.
"""

import csv
import json


def load_csv(input_filepath):
    """
    This function will load a csv from the given file.
    :param input_filepath: String, location of the given file
    :return: A dictionary representation of the csv file
    """
    # Read the CSV file
    csv_data = []
    with open(input_filepath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Read each row into the dictionary
        for row in csv_reader:
            csv_data.append(row)

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

