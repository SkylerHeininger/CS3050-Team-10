"""
Skyler Heininger
CS 3050
This script will upload data to firebase, ensuring that all files exist and are correctly formatted.
"""


import firebase_admin
from firebase_admin import credentials, db
import json
import sys
import os


def connect_firebase(key_path, database_url):
    """
    This method connects to the firebase
    :param key_path: Path to the credentials file
    :param database_url: String path to database
    :return: Null, but establishes firebase app
    """
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred, {'databaseURL': database_url})


def firebase_ref_path(reference_path):
    """
    This function establishes what "file" to interact with in the database, and returns the proper object
    to interact with it
    :param reference_path: String, the reference path in the database
    :return: db reference object
    """
    return db.reference(reference_path)


def check_files_exist(file_paths):
    """
    Check if all the provided files exist
    :param file_paths: List of file paths to check
    :return: Boolean, true if all files exist and false if not
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            return False

    return True


def load_data_to_firebase(data_path, reference_path):
    """
    This will load data from the json to the firebase.
    :param data_path:
    :param reference_path:
    :return: Boolean, true if worked
    """
    # Create database reference
    ref = firebase_ref_path(reference_path)

    # Some basic error handling for firebase
    try:
        # Load data from json
        with open(data_path, "r") as f:
            file_contents = json.load(f)
        ref.set(file_contents)
        return True
    except Exception as e:
        print(f"Firebase failed:\n{e}")
        return False


if __name__ == "__main__":
    # Handle command-line arguments
    if len(sys.argv) != 2:
        print("Need one command line argument")
        sys.exit(1)
    else:
        data_path_arg = sys.argv[1]

    # Ensure provided file exists and the certification file exists
    if not check_files_exist([data_path_arg, "firebase_cert.json"]):
        print("Provided files do not exist, ensure provided file path is correct "
              "and firebase certification is in correct folder")
        sys.exit(2)

    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")

    # Load data to firebase - set universities to correct thing
    data_uploaded = load_data_to_firebase(data_path_arg, "/universities")

    # Final output
    if data_uploaded:
        print("Data successfully uploaded")
    else:
        print("\nData upload failed, please try again.")




