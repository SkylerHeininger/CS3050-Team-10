"""
University.py holds the university class that we will be working with
The class mostly just holds points of data but does have a non-trivial to_string to help with displaying information
"""


class University:
    def __init__(self, rank, university, overall_score, academic_reputation, employer_reputation,
                 faculty_student_ratio, citations_per_faculty, international_faculty_ratio,
                 international_students_ratio, international_research_network, employment_outcomes,
                 sustainability, equal_rank, country, founding_date, student_population):
        self.rank = int(rank)
        self.university = university
        self.overall_score = overall_score
        self.academic_reputation = academic_reputation
        self.employer_reputation = employer_reputation
        self.faculty_student_ratio = faculty_student_ratio
        self.citations_per_faculty = citations_per_faculty
        self.international_faculty_ratio = international_faculty_ratio
        self.international_students_ratio = international_students_ratio
        self.international_research_network = international_research_network
        self.employment_outcomes = employment_outcomes
        self.sustainability = sustainability
        self.equal_rank = equal_rank
        self.country = country
        self.founding_date = founding_date
        self.student_population = student_population

    def generate_university_str(self, field_list) -> str:
        """
        generate_university_str takes a field list argument and returns
        a string that can be used to display specific details about the university.
        """
        to_return = 'Rank: ' + str(self.rank) + ', '
        to_return += 'Name: ' + self.university + ', '

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

    def to_dict(self):
        return {
            'rank': self.rank,
            'university': self.university,
            'overall_score': self.overall_score,
            'academic_reputation': self.academic_reputation,
            'employer_reputation': self.employer_reputation,
            'faculty_student_ratio': self.faculty_student_ratio,
            'citations_per_faculty': self.citations_per_faculty,
            'international_faculty_ratio': self.international_faculty_ratio,
            'international_students_ratio': self.international_students_ratio,
            'international_research_network': self.international_research_network,
            'employment_outcomes': self.employment_outcomes,
            'sustainability': self.sustainability,
            'equal_rank': self.equal_rank,
            'country': self.country,
            'founding_date': self.founding_date,
            'student_population': self.student_population
        }

    @staticmethod
    def from_dict(source):
        """
        Creates an instance of this class using a dictionary.
        :param source: Dictionary of university object
        :return: University object
        """
        if not source['equal_rank']:
            source['equal_rank'] = False
        else:
            source['equal_rank'] = True
        return University(
            int(source['rank']),
            source['university'],
            float(source['overall_score']),
            float(source['academic_reputation']),
            float(source['employer_reputation']),
            float(source['faculty_student_ratio']),
            float(source['citations_per_faculty']),
            float(source['international_faculty_ratio']),
            float(source['international_students_ratio']),
            float(source['international_research_network']),
            float(source['employment_outcomes']),
            float(source['sustainability']),
            source['equal_rank'],
            source['country'],
            int(source['founding_date']),
            source['student_population']
        )

    @staticmethod
    def compare_universities_equivalence(university1, university2):
        """
        Compares two university objects for equality in all fields.
        :param university1: First University object
        :param university2: Second University object
        :return: Boolean true if all fields are equivalent, false if anything is not equivalent.
        """
        return (university1.rank == university2.rank and
                university1.university == university2.university and
                university1.overall_score == university2.overall_score and
                university1.academic_reputation == university2.academic_reputation and
                university1.employer_reputation == university2.employer_reputation and
                university1.faculty_student_ratio == university2.faculty_student_ratio and
                university1.citations_per_faculty == university2.citations_per_faculty and
                university1.international_faculty_ratio == university2.international_faculty_ratio and
                university1.international_students_ratio == university2.international_students_ratio and
                university1.international_research_network == university2.international_research_network and
                university1.employment_outcomes == university2.employment_outcomes and
                university1.sustainability == university2.sustainability and
                university1.equal_rank == university2.equal_rank and
                university1.country == university2.country and
                university1.founding_date == university2.founding_date and
                university1.student_population == university2.student_population)

    @staticmethod
    def compare_universities_field(university1, university2, field):
        """
        This function will compare two university objects by the specified field. This will return
        -1 if the first is less than the second, 0 if equal, and 1 if the first is greater than the second.
        This function is for sorting purposes only. If the field is a string, these will be compared lexicographically.
        Equal objects will also be compared lexicographically by their university name.
        :param university1: University object
        :param university2: University object
        :param field: Field parameter
        :return: 1, 0, -1
        """
        # Convert to dicts, easier accessing fields
        dict_repr_1 = university1.to_dict()
        dict_repr_2 = university2.to_dict()

        # Access values and names
        val_1 = dict_repr_1[field]
        val_2 = dict_repr_2[field]
        name_1 = dict_repr_1["name"]
        name_2 = dict_repr_2["name"]

        # Compare (in python <, > compare lexicographically)
        if val_1 < val_2:
            return -1
        elif val_1 > val_2:
            return 1
        else:
            # Values equal, compare names
            if name_1 < name_2:
                return -1
            elif name_1 > name_2:
                return 1
            else:
                return 0

    # def generate_university_str_default(self) -> str:
    #     """
    #     generate_university_str_default calls generate_university_str with an empty list
    #     to return the default (least detailed) string to describe the university
    #     """
    #     return display_university([])



