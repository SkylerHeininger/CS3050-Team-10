"""
University.py holds the university class that we will be working with
The class mostly just holds points of data but does have a non-trivial to_string to help with displaying information
"""

class University:
    def __init__(self, data_list):
        self.rank = int(data_list[0])
        self.name = data_list[1]
        self.overall_score = data_list[2]
        self.academic_reputation = data_list[3]
        self.employer_reputation = data_list[4]
        self.faculty_student_ratio = data_list[5]
        self.citations_per_faculty = data_list[6]
        self.international_faculty_ratio = data_list[7]
        self.international_students_ratio = data_list[8]
        self.international_research_network = data_list[9]
        self.employment_outcomes = data_list[10]
        self.sustainability = data_list[11]
        self.equal_rank = data_list[12]
        self.country = data_list[13]
        self.founding_date = data_list[14]
        self.student_population = data_list[15]
        
    def generate_university_str(self, field_list) -> str:
        """
        generate_university_str takes a field list argument and returns
        a string that can be used to display specific details about the university.
        """
        to_return = 'Rank: ' + str(self.rank) + ', '
        to_return += 'Name: ' + self.name + ', '

        if 'overall_score' in field_list:
            to_return += 'Overall Score: ' + self.overall_score + ', '
        if 'academic_reputation' in field_list:
            to_return += 'Academic Reputation: ' + self.academic_reputation + ', '
        if 'employer_reputation' in field_list:
            to_return += 'Employer Reputation: ' + self.employer_reputation + ', '
        if 'faculty_student_ratio' in field_list:
            to_return += 'Faculty to Student Ratio: ' + self.faculty_student_ratio + ', '
        if 'citations_per_faculty' in field_list:
            to_return += 'Citations per faculty: ' + self.citations_per_faculty + ', '
        if 'international_faculty_ratio' in field_list:
            to_return += 'International Faculty Ratio: ' + self.international_faculty_ratio + ', '
        if 'international_students_ratio' in field_list:
            to_return += 'International Students Ratio: ' + self.international_students_ratio + ', '
        if 'international_research_network' in field_list:
            to_return += 'International Research Network: ' + self.international_research_network + ', '
        if 'employment_outcomes' in field_list:
            to_return += 'Employment Outcomes: ' + self.employment_outcomes + ', '
        if 'sustainability' in field_list:
            to_return += 'Sustainability: ' + self.sustainability + ', '
        if 'equal_rank' in field_list:
            to_return += 'Equal Rank Flag: ' + self.equal_rank + ', '
        if 'country' in field_list:
            to_return += 'Country: ' + self.country + ', '
        if 'founding_date' in field_list:
            to_return += 'Founding Year: ' + self.founding_date + ', '
        if 'student_population' in field_list:
            to_return += 'Student Population: ' + self.student_population + ', '

        # strip unnecessary commas and spaces
        to_return.rstrip()
        to_return.rstrip(',')

        return to_return
        
    def generate_university_str_default(self) -> str:
        """
        generate_university_str_default calls generate_university_str with an empty list
        to return the default (least detailed) string to describe the university
        """
        return display_university([])
