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
from warmup_utilities import check_files_exist, connect_firebase, firestore_collection_ref



def test_query_engine():
    """
    This method is present for testing the query engine
    :return: true or false, true if passed all test cases
    """
    print("Testing query engine")

    amount_failed = 0
    amount_passed = 0
    number_of_cases = 5

    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")

    # Get reference to firebase Universities
    firestore_collection = firestore.client().collection("universities")

    # Testing values
    conditionals_test_1 = [("rank", "<=", 10), ("rank", ">=", 1)]  # query same field, with overlap
    conditionals_test_2 = [("rank", ">=", 10), ("rank", "==", 1)]  # query same field, no overlap
    conditionals_test_3 = [("rank", "<=", 10), ("academic_reputation", "==", 100)]  # query different fields, likely overlap
    conditionals_test_4 = [("rank", "<=", 10), ("founding_date", ">=", 1800),
                           ("academic_reputation", "==", 100)]  # query 3 fields
    conditionals_test_5 = [("rank", "<=", 10), ("founding_date", ">=", 1900),
                           ("academic_reputation", "==", 100)]  # query 3 fields, with later date out of scope

    # Perform queries
    output_1 = query_engine(conditionals_test_1, firestore_collection)
    output_2 = query_engine(conditionals_test_2, firestore_collection)
    output_3 = query_engine(conditionals_test_3, firestore_collection)
    output_4 = query_engine(conditionals_test_4, firestore_collection)
    output_5 = query_engine(conditionals_test_5, firestore_collection)

    # Check output from queries
    if output_1[0].to_dict()["rank"] == 1 and len(output_1) == 10:
        amount_passed += 1
    else:
        print("[FAILED] Same field overlap failed")
        amount_failed += 1

    if len(output_2) == 0:
        amount_passed += 1
    else:
        print("[FAILED] Same field no overlap failed")
        amount_failed += 1

    if output_3[0].to_dict()["rank"] == 1 and len(output_3) == 6:
        amount_passed += 1
    else:
        print("[FAILED] Different field failed")
        amount_failed += 1

    if output_4[0].to_dict()["rank"] == 1 and len(output_4) == 3:
        amount_passed += 1
    else:
        print("[FAILED] Triple field failed")
        amount_failed += 1

    if len(output_5) == 0:
        amount_passed += 1
    else:
        print("[FAILED] Triple field out of scope failed")
        amount_failed += 1

    if amount_passed == number_of_cases:
        print(f"[PASSED] All {number_of_cases} test cases passed")
        return True
    else:
        print(f"[FAILED] {amount_failed} test cases failed")
        return False


if __name__ == "__main__":
    # Add testing functions as needed. Each one should test the function in several ways, and
    # return true if all test cases passed. If not, print to console what failed and return false at the end of
    # that test suite.
    if test_query_engine():
        print("All test cases passed")
