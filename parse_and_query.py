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

import pyparsing
from pyparsing import one_of # documentation: https://pyparsing-docs.readthedocs.io/en/latest/pyparsing.html
# https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html


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

    where_index = 10000
    display_index = 100000
    sort_index = 100000
    
    # PART 1: detect different keywords that determine what kinds of clauses are in the input string
    # Detect if it is a NAME or SHOW type of query
    if input_string[0, 4].upper == 'NAME':
        is_name = True
    elif input_string[0, 4].upper == 'SHOW':
        is_show = True
    else:
        raise Exception('ERROR IN PARSE: Could not detect query type. Query must start with NAME, SHOW, or HELP')

    # Detect if the query has a WHERE clause
    if 'WHERE' in input_string.upper:
        contains_where = True
        where_index = input_string.upper('WHERE')
    else:
        contains_where = False

    # Detect if the query has a DISPLAY clause
    if 'DISPLAY' in input_string.upper:
        contains_display = True
        display_index = input_string.upper('DISPLAY')
    else:
        contains_display = False

    # Detect if the query has a SORT clause
    if 'SORT' in input_string.upper:
        contains_sort = True
        sort_index = input_string.upper('SORT')
    else:
        contains_sort = False

    # Okay. Now we know if we have each main keyword.
    # This will allow us to more easily go through the rest of the process
    # END OF PART 1

    # Check to make sure the keywords are in the correct order. Further, we know that SHOW or NAME is the first so we don't have to check that
    if contains_where and contains_display and (where_index > display_index):
        # display comes before where which is out of order :(
        raise Exception('ERROR IN PARSE: Where clause comes after display clause.')
    if contains_where and contains_sort and (where_index > sort_index):
        # sort comes before where which is out of order :(
        raise Exception('ERROR IN PARSE: Where clause comes after sort clause.')
    if contains_display and contains_sort and (display_index > sort_index):
        # sort comes before display which is out of order :(
        raise Exception('ERROR IN PARSE: Display clause comes after sort clause.')




    # Use pyparse to separate input string into parts

    # Process and load first part of return tuple (show_int)

    # Process and load second part of return tuple (conditionals)

    # Process and load third part of return tuple (display_list)

    # Process and load last part of return tuple (sort_field)

    # return final tuple


def intersect_lists(list1, list2, comparison_func):
    """
    Compares two lists of university objects using the given comparison function and finds their intersection.
    :param list1: First list of University objects
    :param list2: Second list of University objects
    :param comparison_func: Function to compare two university objects, must return true or false
    :return: Intersection of the two lists based on the comparison function
    """
    intersection = []
    for uni1 in list1:
        for uni2 in list2:
            if comparison_func(uni1, uni2):
                intersection.append(uni1)
                break
    return intersection


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
    #
    query_result_list = []
    for conditional in conditionals:
        # Query using conditional

        # Run .get (also need to run .to_dict on this and then pass that to University.from_dict on each item in the
        # list to get University objects for everything. I highlighted below how to do this

        # Append to query_result_list


    # At this point, query_result_list is like the following: [[object1, object2, object3,...], [...], ...]
    # Loop through and take the first list, compare with the rest of things in list.
    if len(query_result_list) >= 1:
        # Take the first item in the query list(the first thing)
        query_intersect = query_result_list.pop(0)
        while len(query_result_list) >= 1:
            # Take another item and intersect it with the original list, use the University comparison function
            query_intersect = intersect_lists(query_intersect, query_result_list.pop(0),
                                              University.compare_universities)

        return query_intersect
    else:
        # There were no queries performed
        return False

    ''' Old code '''
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
        # TODO: Mason, this is what I meant by above comment, you have to loop through the query documents
        # and create objects for each thing
        universities.append(University.from_dict(doc.to_dict()))
        print(University.from_dict(doc.to_dict()).generate_university_str([]))

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
