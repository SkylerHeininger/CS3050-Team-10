"""
CS 3050 Team 10
This file is for testing the functionality of all the functions of this project
"""
from parse_and_query import query_engine, query_firestore, intersect_lists
from firebase_admin import credentials, db, firestore
import firebase_admin
from firebase_admin import credentials, db
import sys
from google.cloud.firestore_v1 import FieldFilter
import pyparsing

from University import University
from warmup_utilities import firebase_ref_path, check_files_exist, connect_firebase, firestore_collection_ref


def test_query_engine():
    """
    This method is present for testing the query engine
    :return:
    """
    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")

    # Get reference to firebase Universities
    firestore_collection = firestore.client().collection("universities")

    # Ignore this
    # Testing values
    conditionals_test = [("rank", "<=", 10), ("academic_reputation", ">=", 1)]
    # print(firestore_collection.document("University1").get().to_dict())
    print(query_engine(conditionals_test, firestore_collection))




