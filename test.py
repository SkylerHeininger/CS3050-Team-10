"""
CS 3050 Team 10
This file is for testing the functionality of all the functions of this project
"""
from parse_and_query import query_engine, query_firestore, intersect_lists, sorting_engine, \
    merge_sort_universities, print_results
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
    number_of_cases = 8

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
    conditionals_test_6 = [("rank", "<=", 10), ("founding_date", ">=", 2000)]
    conditionals_test_7 = [("rank", "<=", 10), ("people", '>=', 14000)] # invalid field test
    conditionals_test_8 = [("rank", "<=", 10), ("country", '==', "United States")] # country field test

    # Perform queries
    output_1 = query_engine(conditionals_test_1, firestore_collection)
    output_2 = query_engine(conditionals_test_2, firestore_collection)
    output_3 = query_engine(conditionals_test_3, firestore_collection)
    output_4 = query_engine(conditionals_test_4, firestore_collection)
    output_5 = query_engine(conditionals_test_5, firestore_collection)
    output_6 = query_engine(conditionals_test_6, firestore_collection)
    output_7 = query_engine(conditionals_test_7, firestore_collection)
    output_8 = query_engine(conditionals_test_8, firestore_collection)

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

    if len(output_6) == 0:
        amount_passed += 1
    else:
        print("[FAILED] Invalid field")

    if len(output_7) == 0:
        amount_passed += 1
    else:
        print("[FAILED] Invalid field")

    if len(output_8) == 4:
        amount_passed += 1
    else:
        print("[FAILED] Country field failed")

    if amount_passed == number_of_cases:
        print(f"[PASSED] All {number_of_cases} test cases passed for query engine")
        return True
    else:
        print(f"[FAILED] {amount_failed} test cases failed for query engine")
        return False



def test_sort():
    """
    This is sorting function for testing the sorting. This will create a bunch of university objects, sort them,
    and then test that they're sorted. It is important to note that rank is sorted differently from other numeric fields.
    Rather than a higher number being a better number, a lower number is a better one.
    :return: Boolean, true if no test cases failed, false otherwise
    """
    # Get a list of university objects, easiest way to do this is to query using query engine
    print("Testing sorting engine")

    amount_failed = 0
    amount_passed = 0
    number_of_cases = 11

    # Get reference to firebase Universities
    firestore_collection = firestore.client().collection("universities")

    # Testing conditional values
    conditionals = [("rank", "<=", 10), ("rank", ">=", 1)]  # query rank, basic query
    # Different queries will simply give different objects with different values, since we will sort using different
    # fields, then this does not matter

    # Perform query
    output = query_engine(conditionals, firestore_collection)

    # Make sure 10 things are returned - if this is incorrect this is unfixable, there is some other error present
    if len(output) != 10:
        print("[FAILED] Query engine failed for sorting test")
        return False

    # Sort by the following fields - rank is not included in this since it sorts opposite way
    sorting_fields = ["sustainability", "founding_date", "international_faculty_ratio", "academic_reputation"]
    # It is important to note that the parser will automatically limit fields to sort by to only being numerical

    # Set a show_int of 12, decrement and check the length each time
    # This checks that show_int with more items in query in positive direction does not break
    show_int = 12

    # sort each using sorting engine, then loop through to ensure that they are sorted in order
    for field in sorting_fields:
        # sort
        sorted_universities = sorting_engine(output, field, show_int)
        if len(sorted_universities) != show_int and len(sorted_universities) != len(output):
            print("[FAILED] Correct length of university objects")
            amount_failed += 1
        # Loop through the universities and compare each (should be descending order)
        for i in range(len(sorted_universities) - 1):
            if sorted_universities[i].to_dict()[field] < sorted_universities[i + 1].to_dict()[field]:
                print(f"[FAILED] Correctly sorting universities by {field}")
                amount_failed += 1
                break
        show_int -= 1

    # Now do the same but sort negatively
    # Set a show_int of -8, decrement and check the length each time
    # This will additionally test what happens when show_int is set past the max length in negative direction
    show_int = -8

    # sort each using sorting engine, then loop through to ensure that they are sorted in order
    for field in sorting_fields:
        # sort
        sorted_universities = sorting_engine(output, field, show_int)
        # This tests if more things are asked than are in the list
        if len(sorted_universities) != abs(show_int) and len(sorted_universities) != len(output): # abs needed since show_int negative
            print("[FAILED] Correct length of university objects")
            amount_failed += 1
        # Loop through the universities and compare each (should be ascending order)
        for i in range(len(sorted_universities) - 1):
            if sorted_universities[i].to_dict()[field] > sorted_universities[i + 1].to_dict()[field]:
                print(f"[FAILED] Correctly sorting universities by {field}")
                amount_failed += 1
                break
        show_int -= 1

    # test sorting by ranking, with positive show_int
    show_int = 10
    sorted_universities = sorting_engine(output, "rank", show_int)
    if len(sorted_universities) != show_int and len(sorted_universities) != len(output):
        print("[FAILED] Correct length of university objects")
        amount_failed += 1
    # Loop through the universities and compare each (should be ascending order)
    for i in range(len(sorted_universities) - 1):
        if sorted_universities[i].to_dict()["rank"] > sorted_universities[i + 1].to_dict()["rank"]:
            print(f"[FAILED] Correctly sorting universities by rank")
            amount_failed += 1
            break

    # test sorting by ranking, with positive show_int
    show_int = -10
    sorted_universities = sorting_engine(output, "rank", show_int)
    if len(sorted_universities) != show_int and len(sorted_universities) != len(output):
        print("[FAILED] Correct length of university objects")
        amount_failed += 1
    # Loop through the universities and compare each (should be ascending order)
    for i in range(len(sorted_universities) - 1):
        if sorted_universities[i].to_dict()["rank"] < sorted_universities[i + 1].to_dict()["rank"]:
            print(f"[FAILED] Correctly sorting universities by rank")
            amount_failed += 1
            break


    # Now do more edge cases of query has nothing in it
    # Testing conditional values
    conditionals = [("rank", "<", 1)]  # query rank, basic query
    # Different queries will simply give different objects with different values, since we will sort using different
    # fields, then this does not matter

    # Perform query
    output = query_engine(conditionals, firestore_collection)

    # Sort query - random inputs of 100 and rank for the other parameters
    sorted_universities = sorting_engine(output, "rank", 100)
    if sorted_universities != []:
        print("[FAILED] Empty sorted query test case")
        amount_failed += 1

    amount_passed = number_of_cases - amount_failed
    if amount_passed == number_of_cases:
        print(f"[PASSED] All {number_of_cases} test cases passed for sorting engine")
        return True
    else:
        print(f"[FAILED] {amount_failed} test cases failed for sorting engine")
        return False


def test_print():
    """
    This is the printing function for the query output. This will print the queried, sorted, things and this
    will be compared to the correct output.
    :return: Boolean, true if no test cases failed, false otherwise
    """
    print("Testing printing function")
    # Test case variables
    amount_failed = 0
    number_of_cases = 3

    # Strings are returned using this: university.generate_university_str(display_fields)
    # Must check that these are all correct

    # Query to get a single thing
    # Get reference to firebase Universities
    firestore_collection = firestore.client().collection("universities")

    # Testing conditional values
    conditionals = [("rank", "<=", 3), ("rank", ">=", 1)]  # query rank, basic query
    # Different queries will simply give different objects with different values, since we will sort using different
    # fields, then this does not matter

    # Perform query
    output = query_engine(conditionals, firestore_collection)
    # Sort universities, to ensure same workflow as in practice
    sorted_unis = sorting_engine(output, "rank", 100)

    # Test with basic fields
    expected_output_1 = ["Rank: 1, Name: Massachusetts Institute of Technology (MIT), Employer Reputation: 100.0",
                         "Rank: 2, Name: University of Cambridge, Employer Reputation: 100.0",
                         "Rank: 3, Name: University of Oxford, Employer Reputation: 100.0"]
    for i in range(len(sorted_unis)):
        if expected_output_1[i] != sorted_unis[i].generate_university_str(["employer_reputation"]):
            amount_failed += 1
            print("[FAILED] Single display output")
            break

    # Testing conditional values
    conditionals = [("rank", "<=", 38), ("rank", ">=", 33)]  # query rank, basic query
    # Perform query
    output = query_engine(conditionals, firestore_collection)
    # Sort universities, to ensure same workflow as in practice
    sorted_unis = sorting_engine(output, "rank", 100)

    # Test with optional fields and tied in rank
    expected_output_2 = ["Rank: 33, Name: University of Michigan-Ann Arbor, Employer Reputation: 89.9, Not tied in ranking",
                         "Rank: 34, Name: Australian National University (ANU), Employer Reputation: 70.2, Tied in rank at position: 34",
                         "Rank: 34, Name: University of British Columbia, Employer Reputation: 93.5, Tied in rank at position: 34",
                         "Rank: 36, Name: EPFL Ã¢â‚¬â€œ Ãƒâ€°cole polytechnique fÃƒÂ©dÃƒÂ©rale de Lausanne, Employer Reputation: 59.9, Not tied in ranking",
                         "Rank: 37, Name: Technical University of Munich, Employer Reputation: 98.2, Not tied in ranking",
                         "Rank: 38, Name: Institut Polytechnique de Paris, Employer Reputation: 99.6, Tied in rank at position: 38",
                         "Rank: 38, Name: New York University (NYU), Employer Reputation: 98.5, Tied in rank at position: 38"]
    for i in range(len(sorted_unis)):
        if expected_output_2[i] != sorted_unis[i].generate_university_str(["employer_reputation", "equal_rank"]):
            amount_failed += 1
            print("[FAILED] Single display output")
            break

    # Test with no fields provided
    conditionals = [("rank", "<=", 3), ("rank", ">=", 1)]  # query rank, basic query
    # Perform query
    output = query_engine(conditionals, firestore_collection)
    # Sort universities, to ensure same workflow as in practice
    sorted_unis = sorting_engine(output, "rank", 100)

    expected_output_3 = ["Rank: 1, Name: Massachusetts Institute of Technology (MIT)",
                         "Rank: 2, Name: University of Cambridge",
                         "Rank: 3, Name: University of Oxford"]
    for i in range(len(sorted_unis)):
        if expected_output_3[i] != sorted_unis[i].generate_university_str([]):
            amount_failed += 1
            print("[FAILED] Single display output")
            break

    # Print test case results
    amount_passed = number_of_cases - amount_failed
    if amount_passed == number_of_cases:
        print(f"[PASSED] All {number_of_cases} test cases passed for printing function")
        return True
    else:
        print(f"[FAILED] {amount_failed} test cases failed for printing function")
        return False


if __name__ == "__main__":
    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")

    # Add testing functions as needed. Each one should test the function in several ways, and
    # return true if all test cases passed. If not, print to console what failed and return false at the end of
    # that test suite.
    if test_query_engine() and test_sort() and test_print():
        print("All test cases passed")
