"""
CS 3010 Team 10
Warmup project
Shared functions between the admin program and the query system.
"""

import firebase_admin
from firebase_admin import credentials, db, firestore
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


def firestore_collection_ref(reference_path):
    """
    This creates a firestore collection reference. This will be used to query the datastore.
    :param reference_path: string, where the firestore is located in firebase.
    :return: reference object to the collection
    """
    database = firestore.client()
    return database.collection(reference_path)


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
