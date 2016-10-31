import webbrowser
import re
import requests
import bs4


class Parser:
    """
        Parses UCLA's undergraduate major information. Generates a dictionary of majors and their abbreviations.

    """
    def __init__(self):
        """Generates a dictionary consisting of all UCLA undergraduate majors and their abbreviations"""
        with open("Majors.txt", "r") as myfile:
            text = myfile.readlines()

        self.majors = {}

        for lines in text:
            name = re.search("(?<=\t)[A-Z][a-z]+"
                             "(( and| of| in| as a| \|| the|, Study of)*"
                             "( |(\/)|-|, )[A-Z][a-z,]+)*"
                             "( \(undergraduate\))*"
                             "( \(Graduate\))*"
                             "( \(pre-16F\))*"
                             "( \(pre-15F\))*"
                             "(?=\t|  )", lines)
            abbrev = re.search("(?<=\t)([A-Z -\/&])+(?=(\t| )"
                               "(AA|DN|EI|EN|GS|HU|IS|LF|LW|MG|MN|MU|NS|PA|PH|PS|SM|SS|TF)\t)", lines)
            if name and abbrev:
                self.majors.update({name.group(0).lower(): abbrev.group(0)})

        self.majors.update({"religion, study of": "RELIGN", "neuroscience": "NEUROSC",
                           "mechanical and aerospace engineering": "MECH&AE"})

    def convert_symbol(self, string):
        """Converts & to proper symbol"""
        for i in range(len(string)):
            if string[i] == "&":
                return string[0:i] + "%26" + string[i + 1:]
        return string

    def major_abbrev(self, major):
        """Converts input to major abbreviation"""
        output = ""
        if major.upper() in self.majors.values():
            output = self.convert_symbol(major)

        elif major.lower() in self.majors.keys():
            output = self.convert_symbol(self.majors[major.lower()])

        else:
            raise ValueError("Subject area not found")

        return output

    def open_coursedes(self, major):
        """Opens course description website of major"""
        webbrowser.open("http://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=" +
                        self.major_abbrev(major) + "&funsel=3")

    def parse_courses(self, major):
        """Parses course descriptions of major and generates a list of dictionaries, each of which stands for
        a course"""
        raw = requests.get("http://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=" +
                        self.major_abbrev(major) + "&funsel=3")
        page_html = bs4.BeautifulSoup(raw.text, "html.parser")
        courses_html = page_html.find_all(class_="media-body")
        # print(courses_html[1])
        course_list = []

        num2word = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
                    "ten": 10}

        regex_dict = {"Seminar": "(?<=Seminar, )[a-z]+(?= hour)",
                      "Lecture": "(?<=Lecture, )[a-z]+(?= hour)",
                      "Outside study": "(?<=outside study, )[a-z]+(?= hour)",
                      "Laboratory": "(?<=(?:L|l)aboratory, )[a-z]+(?= hour)",
                      "Discussion": "(?<=discussion, )[a-z]+(?= hour)",
                      "Studio": "(?<=Studio, )[a-z]+(?= hour)"
                      }

        for course in courses_html:
            course_dict = {"Number": re.search("[A-Z]*[0-9]+[A-Z]*", course.get_text()).group(0),
                           "Name": re.search("(?<=. )[A-Za-z ]+", course.get_text()).group(0),
                           "Units": re.search("(?<=Units: )[1-9]+", course.get_text()).group(0),
                           "Seminar": 0,
                           "Lecture": 0,
                           "Outside study": 0,
                           "Laboratory": 0,
                           "Discussion": 0,
                           "Studio": 0,
                           "Description": re.search("(?<=[a-z]\. )[A-Z].+", course.get_text()).group(0)
                           }

            for keys, values in regex_dict.items():
                if re.search(values, course.get_text()):
                    course_dict.update({keys: num2word[re.search(values, course.get_text()).group(0)]})

            if re.search("(?<=Lecture\/demonstration, )[a-z]+(?= hour)", course.get_text()):
                course_dict.update({"Lecture": num2word[re.search("(?<=Lecture\/demonstration, )[a-z]+(?= hour)",
                                                                  course.get_text()).group(0)]})

            course_list.append(course_dict)

        print(course_list)


parser = Parser()
parser.parse_courses("bioengineering")
