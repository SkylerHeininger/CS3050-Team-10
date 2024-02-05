"""
CS3010 team 10
Warmup project
This contains the engines for the warmup project, and many other functions.
"""
from firebase_admin import credentials, db, firestore
import firebase_admin
from firebase_admin import credentials, db
import sys
from google.cloud.firestore_v1 import FieldFilter
from University import University

from warmup_utilities import firebase_ref_path, check_files_exist, connect_firebase, firestore_collection_ref

import pyparse  # documentation: https://pyparsing-docs.readthedocs.io/en/latest/pyparsing.html


def parse(input_string):
    """

    :param input_string:
    :return:
    """
    # Create pyparse dictionaries
    valid_conditionals = one_of("== != > < >= <=")
    valid_fields = one_of("rank university overall_score academic_reputation employer_reputation faculty_student_ratio "
                          "citations_per_faculty international_faculty_ratio international_students_ratio "
                          "international_research_network employment_outcomes sustainability equal_rank country "
                          "founding_date student_population")
    
    # PART 1: detect different keywords that determine what kinds of clauses are in the input string
    # Detect if it is a NAME or SHOW type of query
    if input_string[0, 4].upper == 'NAME':
        is_name = True
    elif input_string[0, 4].upper == 'SHOW':
        is_show = True
    elif input_string[0, 4].upper == 'HELP':
        is_help = True
        # TODO: figure out what to do in this situation. I (Ethan R) think we should immediately return and trigger the other function to display the help menu
        # return 'Help!'
    else:
        raise Exception('ERROR IN PARSE: Could not detect query type. Query must start with NAME, SHOW, or HELP')

    # Detect if the query has a WHERE clause
    if 'WHERE' in input_string.upper:
        contains_where = True

    # Detect if the query has a DISPLAY clause
    if 'DISPLAY' in input_string.upper:
        contains_where = True

    # Detect if the query has a SORT clause
    if 'SORT' in input_string.upper:
        contains_sort = True

    # Okay. Now we know if we have each main keyword.
    # This will allow us to more easily go through the rest of the process
    # END OF PART 1

    # Use pyparse to separate input string into parts

    # Process and load first part of return tuple (show_int)

    # Process and load second part of return tuple (conditionals)

    # Process and load third part of return tuple (display_list)

    # Process and load last part of return tuple (sort_field)

    # return final tuple


def query_firestore(conditional, firestore):
    """
    This function will query a single thing
    :param conditional: tuple of size 3, with field, operator, conditional
    :return: The query object for a single conditional
    """
    print(conditional)
    # Filter for the conditional
    filter_cond = FieldFilter(conditional[0], conditional[1], conditional[2])
    # Create a query against the collection
    query_output = firestore.where(filter=filter_cond)
    return query_output


def query_engine(conditionals, firestore):
    """
    This function is the engine that will query the database.
    This will handle multiple conditionals and create a list of objects
    :param conditionals: list of tuples of size 3, with each one having a string field, string operator, and string/int/float value
    :param firestore: reference path to firebase over which queries will be performed
    :return: List of University objects
    """
    # Need to query the firestore multiple times using the .where
    # Query the first thing in conditionals
    query_compound = query_firestore(conditionals.pop(0), firestore)
    while len(conditionals) > 0:
        # Based on the structure, we can update query_result using query_firestore.
        # Each time we call this, it will append another .where() onto the pre-existing query
        query_compound = query_firestore(conditionals.pop(0), query_compound)

    # Now, we use .stream to perform the query and store the results to a tuple
    query_documents = (query_compound.get())
    print(query_documents)
    print(len(query_documents))

    # Create university objects from the documents
    universities = []
    for doc in query_documents:
        print(doc)
        universities.append(University.from_dict(doc.to_dict()))

    return universities


if __name__ == "__main__":
    # Initialize firebase app, making sure that firebase certification is present
    # This is done before the user starts querying since throwing this error later would be a worse user experience
    if not check_files_exist(["firebase_cert.json"]):
        print("Provided files do not exist, ensure the firebase certification is in correct folder")
        sys.exit(2)

    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")

    # Get reference to firebase Universities
    firestore_collection = firestore.client().collection("universities")

    # Testing values
    conditionals = [("rank", "<=", 10)]
    # print(firestore_collection.document("University1").get().to_dict())
    print(query_engine(conditionals, firestore_collection))

    sys.exit()
    # Loop to query user until they exit
    query_string = ""
    while query_string != "exit":
        # Get input from user
        user_input = input(">> ")  # Format this however we want

        # If input is exit or help, handle those and continue to next loop

        # Pass input to parser

        # Pass parser conditionals to query

        # Pass query objects to sort function

        # Pass sorted objects to print function
