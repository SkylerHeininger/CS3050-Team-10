"""
CS 3010 Team 10
Warmup project
Shared functions between the admin program and the query system.
"""
import sys

import firebase_admin
from firebase_admin import credentials, db, firestore
from firebase_admin.exceptions import NotFoundError
import os


def connect_firebase(key_path, database_url):
    """
    This method connects to the firebase. This has a hard stop to the program if the firebase is not
    connected to, as this is a un-recoverable issue. Since this is hard-coded into the warmup
     project, this does not depend on user input and is more an overall code clean-up strategy.
    :param key_path: Path to the credentials file
    :param database_url: String path to database
    :return: Null, but establishes firebase app
    """
    try:
        cred = credentials.Certificate(key_path)
    except:
        print("Please ensure that your firebase certificate is in the correct location.")
        sys.exit(1)
    try:
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})
    except:
        print("Please ensure that the database url is correct, then try again.")
        sys.exit(1)


def firestore_collection_ref(reference_path):
    """
    This creates a firestore collection reference. This will be used to query the datastore.
    This method will fail if the reference path is not correct. Since this is hard-coded
    into the warmup project, this does not depend on user input and is more an overall code clean-up strategy.
    :param reference_path: string, where the firestore is located in firebase.
    :return: reference object to the collection
    """
    try:
        database = firestore.client()
        return database.collection(reference_path)
    except NotFoundError:
        print("The supplied reference path was not found, please try again.")
        sys.exit(1)
    except:
        print("An error occurred, please try again.")
        sys.exit(1)


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
