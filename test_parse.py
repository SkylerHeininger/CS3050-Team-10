from pyparsing import one_of

def test_parse():
    print(parse('show 10 where rank >= 6 and overall_score <5'))
    print(parse('name uvmletsgooo where pee pee poo poo'))
    #print(parse('WH ;KLASDF;KLJ WHERE ;LKASD;LKASD SORT ;ALSKDF'))


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
    valid_fields_dictionary = {"rank": "num", "university": "string", "overall_score": "num",
                               "academic_reputation": "num",
                               "employer_reputation": "num", "faculty_student_ratio": "num",
                               "citations_per_faculty": "num", "international_faculty_ratio": "num",
                               "international_students_ratio": "num",
                               "international_research_network": "num", "employment_outcomes": "num",
                               "sustainability": "num",
                               "equal_rank": "num", "country": "string", "founding_date": "num"}

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
            raise Exception("Invalid input for show int")

    # Process and load second part of return tuple (conditionals)
    # start by splitting into different conditional phrases
    conditional_string_list: list[str] = query_dict['where_phrase'].split("and")
    conditional_list_list: list[list] = []  # will use this to work with each part of a compound conditional input
    conditional_tuple_list: list[tuple] = []  # will use a tuple to finalize and return the conditionals

    # go through each conditional phrase list and find what kind of conditional it is
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
                    single_conditional_tuple = (single_conditional_list[0], single_conditional_list[1], single_conditional_list[2])
                    conditional_tuple_list.append(single_conditional_tuple)
                except ValueError:  # couldn't be cast. Raise Exception
                    raise Exception("Can't cast", single_conditional_list[2], "to a float when comparing to",
                                    single_conditional_list[0], "field")
        else:
            print("couldn't find a valid field corresponding to the argument \'", single_conditional_list[0])

    print(conditional_list_list)



def main():
    test_string = "Hello and where but and poop"
    print(test_string.split("and"))
    test_parse()


main()

