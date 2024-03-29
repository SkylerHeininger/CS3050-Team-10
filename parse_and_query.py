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


# import pyparsing
# from pyparsing import one_of  # documentation: https://pyparsing-docs.readthedocs.io/en/latest/pyparsing.html


# https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html


def parse(input_string):
    """

    :param input_string:
    :return:
    """
    valid_conditionals_list = ["==", "!=", ">=", "<=", ">", "<"]
    valid_fields_dictionary = {"rank": "num", "university": "string", "overall_score": "num",
                               "academic_reputation": "num",
                               "employer_reputation": "num", "faculty_student_ratio": "num",
                               "citations_per_faculty": "num", "international_faculty_ratio": "num",
                               "international_students_ratio": "num",
                               "international_research_network": "num", "employment_outcomes": "num",
                               "sustainability": "num",
                               "equal_rank": "string", "country": "string", "founding_date": "num",
                               "student_population": "num"}
    # equal rank is not a string but the code will handle it correctly if we call it a string here

    where_index = 10000
    display_index = 100000
    sort_index = 100000

    RETURN_ERROR_TUPLE = ('error', 'error', 'error', 'error')  # use to return when we run into an issue

    # PART 1: detect different keywords that determine what kinds of clauses are in the input string
    # Detect if it is a NAME or SHOW type of query
    if input_string[0: 4].upper() == 'NAME':
        is_name = True
        is_show = False
    elif input_string[0: 4].upper() == 'SHOW':
        is_show = True
        is_name = False
    else:
        print("ERROR IN PARSE: Could not detect query type. Query must start with NAME, SHOW, or HELP")
        return RETURN_ERROR_TUPLE

    # Detect if the query has a WHERE clause
    if 'WHERE' in input_string.upper():
        contains_where = True
        where_index = input_string.upper().find('WHERE')
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
        print('ERROR IN PARSE: Where clause comes after display clause.')
        return RETURN_ERROR_TUPLE
    if contains_where and contains_sort and (where_index > sort_index):
        # sort comes before where which is out of order :(
        print('ERROR IN PARSE: Where clause comes after sort clause.')
        return RETURN_ERROR_TUPLE
    if contains_display and contains_sort and (display_index > sort_index):
        # sort comes before display which is out of order :(
        print('ERROR IN PARSE: Display clause comes after sort clause.')
        return RETURN_ERROR_TUPLE

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
    # print(query_dict)
    # remove the start of part keywords from the query_dict
    query_dict['name_or_show_phrase'] = query_dict['name_or_show_phrase'][len('SHOW'):]
    if query_dict['where_phrase'] != '':
        query_dict['where_phrase'] = query_dict['where_phrase'][len('WHERE'):]
    if query_dict['display_phrase'] != '':
        query_dict['display_phrase'] = query_dict['display_phrase'][len('DISPLAY'):]
    if query_dict['sort_phrase'] != '':
        query_dict['sort_phrase'] = query_dict['sort_phrase'][len('SORT'):]
    # print(query_dict)

    # Process and load first part of return tuple (show_int)
    name_show = (str(query_dict['name_or_show_phrase']).strip()).upper()

    if is_show:
        try:
            name_show = int(name_show)
        except:
            if name_show == '-*' or name_show == '-ALL':
                name_show = -106
            elif name_show == '*' or name_show == 'ALL':
                name_show = 106
            else:
                name_show = 'error'

    if is_name:
        # if it is a name-type query, create a conditional based on the name
        query_dict['where_phrase'] = "university == " + query_dict['name_or_show_phrase']
        name_show = 1

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
                conditional_list_list.append(
                    [single_conditional_list[0], conditional_operator, single_conditional_list[1]])
                found_valid_conditional = True

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

        if found_valid_field:
            # figure out what kind of comparisons we can do with the value we are comparing
            field_type = valid_fields_dictionary[single_conditional_list[0]]
            # if we are comparing a string, make sure we are just using == or !=
            if field_type == "string":
                if single_conditional_list[1] != "==" and single_conditional_list[1] != "!=":
                    # user is trying to use an inequality on a string field. return error
                    print("Invalid Comparison. Can't use and inequality to evaluate",
                          single_conditional_list[0], "field")
                    return RETURN_ERROR_TUPLE
                # if we are here, then the string field is being used correctly. Thus we should add to the tuple list
                single_conditional_tuple = (single_conditional_list[0],
                                            single_conditional_list[1],
                                            single_conditional_list[2])
                conditional_tuple_list.append(single_conditional_tuple)

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
                except ValueError:  # couldn't be cast. Raise error
                    print("Can't cast", single_conditional_list[2], "to a float when comparing to",
                          single_conditional_list[0], "field")
                    return RETURN_ERROR_TUPLE
        else:
            print("couldn't find a valid field corresponding to the argument \'", single_conditional_list[0])

    # Process and load third part of return tuple (display_list)
    display_list = []
    for valid_field in valid_fields_dictionary.keys():
        # if junk in hte field, then ignore
        if valid_field in query_dict['display_phrase'].lower():
            display_list.append(valid_field)

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

    # notify user if sort field can't be found, only if it is show-type query
    if not found_valid_field and is_show:
        print('Could not find a valid field to sort by. Will sort by default field: rank')
        sort_field = 'rank'

    # return final tuple
    to_return = (name_show, conditional_tuple_list, display_list, sort_field)
    # print('returning from parse: ', to_return)
    return to_return


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
    try:
        # Filter for the conditional
        filter_cond = FieldFilter(conditional[0], conditional[1], conditional[2])
        # Create a query against the collection
        query_output = firestore.where(filter=filter_cond)
        return query_output
    except Exception as e:
        print("Error while querying, please try again")
        return "error"  # string that won't be falsy or seen in output


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
        if query_output == 'error':
            return 'error'  # Early stopping, return string that won't be considered falsy

        # Query using nth conditional
        for doc in query_output.get():
            # Convert document into Uni object and append university_object to query_results
            query_results.append(University.from_dict(doc.to_dict()))

        # Append query_results list to query_result_list, repeat process if there is more than one conditional
        query_result_list.append(query_results)

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
        return []


def merge_sort_universities(universities_list, field):
    """
    This function will apply the merge sort algorithm over the universities list to sort them appropriately.
    This used the following merge sort implementation as a reference: https://www.geeksforgeeks.org/merge-sort/
    :param universities_list: List of university objects
    :param field: Field over which to sort
    :return: Sorted list of university objects
    """
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
        # Copy data to temp arrays left[] and right[]
        while i < len(left) and j < len(right):
            comparison = University.compare_universities_field(left[i], right[j], field)
            if comparison < 0 or comparison == 0:
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
        # Account for rank sorting opposite direction than normal
        # This is ascending order when show_int is positive
        if ranking_field == "rank":
            if abs(show_int) > len(universities_sorted):
                show_int = -len(universities_sorted)
            return universities_sorted[:abs(show_int)]
        else:
            # reverse the list to descending order
            universities_sorted = universities_sorted[::-1]
            # check for maximum length
            if show_int > len(universities_sorted):
                show_int = len(universities_sorted)
            return universities_sorted[:abs(show_int)]
    elif show_int < 0:
        # Again, account for rank being opposite
        if ranking_field == "rank":
            # reverse the list to descending order
            universities_sorted = universities_sorted[::-1]
            # check for maximum length
            if show_int > len(universities_sorted):
                show_int = len(universities_sorted)
            return universities_sorted[:abs(show_int)]
        else:
            if abs(show_int) > len(universities_sorted):
                show_int = -len(universities_sorted)
            return universities_sorted[:abs(show_int)]
    else:
        # return an empty list if a show_int of 0 is provided
        return []


def print_results(universities_list, display_fields):
    """
    This function prints the the results of the query.
    :param universities_list: The queried and sorted list of University objects
    :param display_fields: The fields to display
    :return: Boolean of if the items printed correctly or not. This is more for helping testing than with functionality.
    """
    # Handle empty query list
    if universities_list == []:
        print("Query resulted in no universities.")
        return True

    for university in universities_list:
        try:
            print(university.generate_university_str(display_fields))
        except Exception as e:
            print("Error occurred, please try again")
            return False
    return True


def print_help():
    """
    This function will print the help output to the console
    :return: Null
    """
    output_string = f"Here are some commands with their uses:\n" \
                    f"show - how many items to return, make this negative for descending order\n" \
                    f"     - make show negative to reverse the order of outputn\n" \
                    f"     - all or * will return all items\n" \
                    f"name - the name of the university to return information on\n" \
                    f"     - conditionals and sorting will be ignored\n" \
                    f"where - the conditionals over which you want to compare universities, separate conditionals using 'and'\n" \
                    f"display - the fields you wish to have displayed to console\n" \
                    f"sort - the field over which you want the output to be sorted, defaults to ranking\n" \
                    f"\nQueries need to be in the order name/show, where, display,sort. Example:\n" \
                    f"show 10 where rank <= 10 display sustainability sort faculty_student_ratio\n" \
                    f"name Columbia University display international_research_network\n"
    print(output_string)


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
        user_input = input("\n>> ")  # Format this however we want

        # If input is exit or help, handle those and continue to next loop
        if user_input.strip()[:4].upper() == "HELP":
            print_help()
            continue
        elif user_input.strip()[:4].upper() == "EXIT":
            print("Exiting query program.")
            break

        # Pass input to parser
        show_int, conditionals, display_fields, sorting_field = parse(user_input)

        # If error, don't pass to query
        if show_int == "error" or conditionals == "error" or display_fields == "error" or sorting_field == "error":
            continue

        # Pass parser conditionals to query
        query_results = query_engine(conditionals, firestore_collection)

        # Handle error in query engine
        if query_results == 'error':
            # print("An error occurred, please try again")
            continue

        # Pass query objects to sort function
        sorted_results = sorting_engine(query_results, sorting_field, show_int)

        # Pass sorted objects to print function - don't really need to use the boolean output
        # since it will re-prompt anyways
        print_results(sorted_results, display_fields)

"""
name Columbia University display sustainability, founding_date
show all where university == Columbia University display sustainability, founding_date

show all where rank <= 10 
show -all where rank <= 10 

show 5 where rank <= 10 and country == United States
show 5 where sustainability >= 90 display sustainability sort sustainability

show -10 where faculty_student_ratio < 50 and student_population > 10000 display student_population, founding_date
show -10 where faculty_student_ratio < 50 and student_population > 10000 display student_population, founding_date sort employment_outcomes

show 10 where rank >= 95 display employment_outcomes sort employment_outcomes

"""



