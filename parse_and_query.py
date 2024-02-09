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

from warmup_utilities import check_files_exist, connect_firebase, firestore_collection_ref

import pyparsing
from pyparsing import one_of  # documentation: https://pyparsing-docs.readthedocs.io/en/latest/pyparsing.html


# https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html


def parse(input_string):
    """

    :param input_string:
    :return:
    """
    # Create pyparse dictionaries
    """
    valid_conditionals = one_of("== != > < >= <=")
    valid_fields = one_of("rank university overall_score academic_reputation employer_reputation faculty_student_ratio "
                          "citations_per_faculty international_faculty_ratio international_students_ratio "
                          "international_research_network employment_outcomes sustainability equal_rank country "
                          "founding_date student_population")"""
    valid_conditionals_list = ["==", "!=", ">=", "<=", ">", "<"]
    valid_fields_dictionary = {"rank": "num", "university": "string", "overall_score": "num", "academic_reputation": "num",
                               "employer_reputation": "num", "faculty_student_ratio": "num",
                               "citations_per_faculty": "num", "international_faculty_ratio": "num", "international_students_ratio": "num",
                               "international_research_network": "num", "employment_outcomes": "num", "sustainability": "num",
                               "equal_rank": "num", "country": "string" ,"founding_date": "num"}

    where_index = 10000
    display_index = 100000
    sort_index = 100000

    # PART 1: detect different keywords that determine what kinds of clauses are in the input string
    # Detect if it is a NAME or SHOW type of query
    if input_string[0: 4].upper() == 'NAME':
        is_name = True
        is_show = False
    elif input_string[0: 4].upper() == 'SHOW':
        is_show = True
        is_name = False
    else:
        raise Exception('ERROR IN PARSE: Could not detect query type. Query must start with NAME, SHOW, or HELP')

    # Detect if the query has a WHERE clause
    if 'WHERE' in input_string.upper():
        contains_where = True
        where_index = input_string.upper().find('WHERE')
        print('where index: ', where_index)
    else:
        contains_where = False

    # Detect if the query has a DISPLAY clause
    if 'DISPLAY' in input_string.upper():
        contains_display = True
        display_index = input_string.upper().find('DISPLAY')
    else:
        contains_display = False

    # Detect if the query has a SORT clause
    if 'SORT' in input_string.upper():
        contains_sort = True
        sort_index = input_string.upper().find('SORT')
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

    # Use separate input string into parts of query
    # first do part 1
    # ???? does same thing if name or show

    end_index = min(where_index, display_index, sort_index, len(input_string))
    query_part_1 = input_string[0: end_index]

    # now do WHERE section
    if contains_where:
        start_index = len(query_part_1)  # calc start index
        end_index = min(display_index, sort_index, len(input_string))  # calc end index
        query_part_2 = input_string[start_index: end_index]
    else:
        query_part_2 = ''

    # now do DISPLAY section
    if contains_display:
        start_index = len(query_part_1 + query_part_2)  # calc start index
        end_index = min(sort_index, len(input_string))  # calc end index
        query_part_3 = input_string[start_index: end_index]
    else:
        query_part_3 = ''

    # now do SORT section
    if contains_sort:
        start_index = len(query_part_1 + query_part_2 + query_part_3)  # calc start index
        end_index = len(input_string)
        query_part_4 = input_string[start_index: end_index]
    else:
        query_part_4 = ''

    # pack into dict
    query_dict = {'name_or_show_phrase': query_part_1, 'where_phrase': query_part_2, 'display_phrase': query_part_3,
                  'sort_phrase': query_part_4}
    #print(query_dict)
    # remove the start of part keywords from the query_dict
    query_dict['name_or_show_phrase'] = query_dict['name_or_show_phrase'][len('SHOW'):]
    if query_dict['where_phrase'] != '':
        query_dict['where_phrase'] = query_dict['where_phrase'][len('WHERE'):]
    if query_dict['display_phrase'] != '':
        query_dict['display_phrase'] = query_dict['display_phrase'][len('DISPLAY'):]
    if query_dict['sort_phrase'] != '':
        query_dict['sort_phrase'] = query_dict['sort_phrase'][len('SORT'):]
    #print(query_dict)

    # Process and load first part of return tuple (show_int)
    name_show = (str(query_dict['name_or_show_phrase']).strip()).upper()
    if is_show:
        try:
            name_show = int(name_show)
        except:
            raise Exception("Invalid input for show int")

    # Process and load second part of return tuple (conditionals)
    # start by splitting into different conditional phrases
    conditional_string_list: list[str] = query_dict['where_phrase'].split("and")
    conditional_list_list: list[list] = []  # will use this to work with each part of a compound conditional input
    conditional_tuple_list: list[tuple] = []  # will use a tuple to finalize and return the conditionals

    # go through each conditional phrase list and find what kind of conditional it is
    # if there is not a valid conditional operator, it will ignore the phrase
    for single_conditional_string in conditional_string_list:
        found_valid_conditional = False  # will be set to true when we find a valid conditional for this phrase
        for conditional_operator in valid_conditionals_list:  # loop thru valid conditionals to find a valid comparison operator
            if not found_valid_conditional and not single_conditional_string.find(conditional_operator) == -1:
                # the conditional operator is in the conditional phrase string. Split and assign homes to each part
                single_conditional_list = single_conditional_string.split(conditional_operator)
                # create a new tuple entry
                conditional_list_list.append([single_conditional_list[0], conditional_operator, single_conditional_list[1]])
                found_valid_conditional = True

    print(conditional_list_list)

    # now we should go through the tuple list to clean things up (remove whitespace)
    for single_conditional_list in conditional_list_list:
        single_conditional_list[0] = single_conditional_list[0].strip()
        single_conditional_list[2] = single_conditional_list[2].strip()

    # now we need to check if we can do the actual comparison (this is a little more annoying)
    for single_conditional_list in conditional_list_list:
        found_valid_field = False
        for field in valid_fields_dictionary.keys():
            if field in single_conditional_list[0] and not found_valid_field:
                single_conditional_list[0] = field
                found_valid_field = True

        print(single_conditional_list, found_valid_field)
        if found_valid_field:
            # figure out what kind of comparisons we can do with the value we are comparing
            field_type = valid_fields_dictionary[single_conditional_list[0]]
            # if we are comparing a string, make sure we are just using == or !=
            if field_type == "string":
                if single_conditional_list[1] != "==" and single_conditional_list[1] != "!=":
                    # user is trying to use an inequality on a string field. Raise exception
                    raise Exception("Invalid Comparison. Can't use and inequality to evaluate",
                                    single_conditional_list[0], "field")

            else:  # field type is a number. Ensure the value they are comparing to can be cast to a float
                try:
                    # cast to float and put back into list
                    single_conditional_list[2] = float(single_conditional_list[2])

                    # if we are here, the field is valid, and so is the comparison value. Thus
                    # we must pack it into a tuple and add it to the final list of conditional tuples
                    single_conditional_tuple = (single_conditional_list[0],
                                                single_conditional_list[1],
                                                single_conditional_list[2])
                    conditional_tuple_list.append(single_conditional_tuple)
                except ValueError:  # couldn't be cast. Raise Exception
                    raise Exception("Can't cast", single_conditional_list[2], "to a float when comparing to",
                                    single_conditional_list[0], "field")
        else:
            print("couldn't find a valid field corresponding to the argument \'", single_conditional_list[0])

    print(conditional_list_list)


    # Process and load third part of return tuple (display_list)

    # Process and load last part of return tuple (sort_field)
    # see if there is a valid field in the sort field
    sort_field = 'rank'  # rank is the default field to sort by
    found_valid_field = False
    for field in valid_fields_dictionary.keys():
        if field in query_dict['sort_phrase'] and not found_valid_field:
            sort_field = field
            found_valid_field = True

    # check to make sure we can actually sort by that field
    if valid_fields_dictionary[sort_field] == "string":
        print("Can't sort by a string.")
        found_valid_field = False

    if not found_valid_field:
        print('Could not find a valid field to sort by. Will sort by default field: rank')
        sort_field = 'rank'

    print('sort field:', sort_field)

    # return final tuple
    return (name_show, conditional_tuple_list, [''], sort_field)


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
                # Break out of the inner list since this item has already been intersected -
                # There is no point to continuing with this inner loop
                break
    return intersection


def query_firestore(conditional, firestore):
    """
    This function will query a single thing
    :param conditional: tuple of size 3, with field, operator, conditional
    :return: The query object for a single conditional
    """
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

    query_result_list = []
    for conditional in conditionals:
        # Create list to store docs queried for nth conditional in conditionals
        query_results = []

        # Query using query_firestore
        query_output = query_firestore(conditional, firestore)

        # Query using nth conditional
        for doc in query_output.get():
            # # Convert document into Uni object (???)
            # university_object = doc.from_dict(doc.to_dict())
            #
            # # Append university_object to query_results
            # query_results.append(university_object)

            query_results.append(University.from_dict(doc.to_dict()))

        # Append query_results list to query_result_list, repeat process if there is more than one conditional
        query_result_list.append(query_results)


        # Query using conditional
        pass
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
                                              University.compare_universities_equivalence)

        return query_intersect
    else:
        # There were no queries performed
        return False


def merge_sort_universities(universities_list, field):
    """
    This function will apply the merge sort algorithm over the universities list to sort them appropriately.
    This used the following merge sort implementation as a reference: https://www.geeksforgeeks.org/merge-sort/
    :param universities_list: List of university objects
    :param field: Field over which to sort
    :return: Sorted list of university objects
    """
    # TODO: test this function to ensure functionality
    if len(universities_list) > 1:
        # Find middle of array
        middle = len(universities_list) // 2
        # Divide the array into two sides
        left = universities_list[:middle]
        right = universities_list[middle:]

        # Sort the halves
        left = merge_sort_universities(left, field)
        right = merge_sort_universities(right, field)

        # Initialize sorting variables
        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(left) and j < len(right):
            if University.compare_universities_field(left[i], right[j], field) < 0:
                universities_list[k] = left[i]
                i += 1
            else:
                universities_list[k] = right[j]
                j += 1
            k += 1

        # Checking if any element was left after this sorting step
        while i < len(left):
            universities_list[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            universities_list[k] = right[j]
            j += 1
            k += 1

    return universities_list


def sorting_engine(universities_list, ranking_field, show_int):
    """
    This function will call the merge_sort_universities function and sort the given list of University
    objects using the inputted field as the method of sorting.
    :param universities_list: List of University objects
    :param ranking_field: the field over which to sort
    :param show_int: The number of universities to return, if positive, the highest amount, if negative the least amount
    :return: List of universities of size show_int
    """
    # Sort the universities
    universities_sorted = merge_sort_universities(universities_list, ranking_field)

    # Select the show_int amount of things, in descending order if show_int is positive
    # and ascending order if n is negative
    if show_int > 0:
        return universities_sorted[-show_int:]
    elif show_int < 0:
        return universities_sorted[:show_int]
    else:
        # return an empty list if a show_int of 0 is provided
        return []


def print_results(universities_list, display_fields):
    """
    This function prints the the results of the query.
    :param universities_list: The queried and sorted list of University objects
    :param display_fields: The fields to display
    :return: True if all printing occurred successfully, false otherwise
    """
    for university in universities_list:
        print(university.generate_university_str(display_fields))


if __name__ == "__main__":
    # Initialize firebase app, making sure that firebase certification is present
    # This is done before the user starts querying since throwing this error later would be a worse user experience
    if not check_files_exist(["firebase_cert.json"]):
        print("Provided files do not exist, ensure the firebase certification is in correct folder")
        sys.exit(2)

    # Establish connection with firebase
    connect_firebase("firebase_cert.json", "https://cs3050-10-default-rtdb.firebaseio.com/")
    # Get reference to firebase Universities
    firestore_collection = firestore_collection_ref("universities")

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
