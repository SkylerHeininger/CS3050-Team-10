from pyparsing import one_of

def test_parse():
    print(parse('SHOW 10 where hehe > 6 and bleh <5 display ;lasd;fasd;sortflj'))
    print(parse('NAME ;KLASDF;KLJ WHERE ;LKASD;LKASD SORT ;ALSKDF'))


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
    if is_name:
        # is a name type
        # this is the last character the part_1 substring should go to
        end_index = min(where_index, display_index, sort_index, len(input_string))
        query_part_1 = input_string[0: end_index]
    else:
        # is a show-type
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
    print(query_dict)
    # remove the start of part keywords from the query_dict
    query_dict['name_or_show_phrase'] = query_dict['name_or_show_phrase'][len('SHOW'):]
    if query_dict['where_phrase'] != '':
        query_dict['where_phrase'] = query_dict['where_phrase'][len('WHERE'):]
    if query_dict['display_phrase'] != '':
        query_dict['display_phrase'] = query_dict['display_phrase'][len('DISPLAY'):]
    if query_dict['sort_phrase'] != '':
        query_dict['sort_phrase'] = query_dict['sort_phrase'][len('SORT'):]
    print(query_dict)

    # Process and load first part of return tuple (show_int)
    show_int = (str(query_dict['name_or_show_phrase']).strip()).upper()
    if is_show:
        try:
            show_int = int(show_int)
        except:
            raise Exception("Invalid input")
    print(show_int)


    # Process and load second part of return tuple (conditionals)

    # Process and load third part of return tuple (display_list)

    # Process and load last part of return tuple (sort_field)

    # return final tuple
    pass

def main():
    test_parse()


main()

