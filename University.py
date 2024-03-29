"""
University.py holds the university class that we will be working with
The class mostly just holds points of data but does have a non-trivial to_string to help with displaying information
"""
import sys

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
        to_return += 'Name: ' + str(self.university) + ', '

        if 'overall_score' in field_list:
            to_return += 'Overall Score: ' + str(self.overall_score) + ', '
        if 'academic_reputation' in field_list:
            to_return += 'Academic Reputation: ' + str(self.academic_reputation) + ', '
        if 'employer_reputation' in field_list:
            to_return += 'Employer Reputation: ' + str(self.employer_reputation) + ', '
        if 'faculty_student_ratio' in field_list:
            to_return += 'Faculty to Student Ratio: ' + str(self.faculty_student_ratio) + ', '
        if 'citations_per_faculty' in field_list:
            to_return += 'Citations per faculty: ' + str(self.citations_per_faculty) + ', '
        if 'international_faculty_ratio' in field_list:
            to_return += 'International Faculty Ratio: ' + str(self.international_faculty_ratio) + ', '
        if 'international_students_ratio' in field_list:
            to_return += 'International Students Ratio: ' + str(self.international_students_ratio) + ', '
        if 'international_research_network' in field_list:
            to_return += 'International Research Network: ' + str(self.international_research_network) + ', '
        if 'employment_outcomes' in field_list:
            to_return += 'Employment Outcomes: ' + str(self.employment_outcomes) + ', '
        if 'sustainability' in field_list:
            to_return += 'Sustainability: ' + str(self.sustainability) + ', '
            # handling of optional field
        if 'equal_rank' in field_list:
            if self.equal_rank:
                to_return += f'Tied in rank at position: {self.rank}, '
            else:
                to_return += f'Not tied in ranking, '
        if 'country' in field_list:
            to_return += 'Country: ' + str(self.country) + ', '
        if 'founding_date' in field_list:
            to_return += 'Founding Year: ' + str(self.founding_date) + ', '
        if 'student_population' in field_list:
            to_return += 'Student Population: ' + str(self.student_population) + ', '

        # strip unnecessary commas and spaces
        to_return = to_return.rstrip()
        to_return = to_return.rstrip(',')

        return to_return

    def generate_university_str_default(self) -> str:
        """
        generate_university_str_default calls generate_university_str with an empty list
        to return the default (least detailed) string to describe the university
        """
        return self.generate_university_str([])

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
        Creates an instance of this class using a dictionary. This also includes some exception
        handling for the conversions, where there could be possible errors. This will exit the program
        if an exception is raised, as this will likely be due to errors in json data or the firestore, and
        not the user.
        :param source: Dictionary of university object
        :return: University object
        """
        # Handling for optional field, convert the empty string of no input to False, otherwise True
        equal_rank = "" if not source['equal_rank'] else True

        # Handling for student population field if it's a string
        student_population = source['student_population']
        if isinstance(student_population, str):
            student_population = int(student_population.replace(',', ''))  # Removing comma and converting to int

        try:
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
                equal_rank,
                source['country'],
                int(source['founding_date']),
                student_population
            )
        except ValueError:
            print("Type conversion failed, try again.")
            sys.exit(1)
        except TypeError:
            print("Type error when creating University object, try again.")
            sys.exit(1)

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
        This function is for sorting purposes only.
        :param university1: University object
        :param university2: University object
        :param field: Field parameter
        :return: 1, 0, -1
        """
        # Convert to dicts, easier accessing fields
        dict_repr_1 = university1.to_dict()
        dict_repr_2 = university2.to_dict()

        # Access values and names
        # This try clause is really here for testing, to ensure that only the correct fields are passed
        # to the query engine. In practice, this won't be thrown.
        try:
            val_1 = dict_repr_1[field]
            val_2 = dict_repr_2[field]
        except KeyError:
            print("Invalid key entered, try again.")
            sys.exit()

        name_1 = dict_repr_1["university"]
        name_2 = dict_repr_2["university"]

        # Compare (in python <, > compare lexicographically)
        if val_1 < val_2:
            return -1
        elif val_1 > val_2:
            return 1
        else:
            return 0




