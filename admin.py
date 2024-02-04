"""
Skyler Heininger
CS 3050
This script will upload data to firebase, ensuring that all files exist and are correctly formatted.
"""


import json
import sys
from warmup_utilities import firebase_ref_path, check_files_exist, connect_firebase
from firebase_admin import credentials, db, firestore
import University


def load_data_to_firebase(data_path, reference_path):
    """
    This will load data from the json to the firebase.
    :param data_path:
    :param reference_path:
    :return: Boolean, true if worked
    """
    # Create database reference
    datab = firestore.client()

    # Some basic error handling for firebase
    try:
        # Load data from json
        # Load data from JSON
        with open(data_path, "r") as f:
            file_contents = json.load(f)
        # TODO: fix input to convert to correct types: float, int, etc
        # Set each object as a separate document in the specified collection
        for doc_id, uni_data in file_contents.items():
            # Assume City is a class similar to the one in your template
            doc_ref = datab.collection("universities").document(doc_id)
            doc_ref.set(uni_data)

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
    data_uploaded = load_data_to_firebase(data_path_arg, "universities")

    # Final output
    if data_uploaded:
        print("Data successfully uploaded")
    else:
        print("\nData upload failed, please try again.")




