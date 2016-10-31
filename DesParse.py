import webbrowser
import re
import requests
import bs4

num2word = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
            "ten": 10}

regex_dict = {"Number": "[A-Z]*[0-9]+[A-Z]*",
              "Name": "(?<=. )[A-Za-z1-9\- ]+",
              "Units": "(?<=Units: )[1-9]+",
              "Description": "(?<=[a-z]\. )[A-Z].+",
              "Seminar": "(?<=Seminar, )[a-z]+(?= hour)",
              "Lecture": "(?<=Lecture, )[a-z]+(?= hour)",
              "Outside study": "(?<=outside study, )[a-z]+(?= hour)",
              "Laboratory": "(?<=(?:L|l)aboratory, )[a-z]+(?= hour)",
              "Discussion": "(?<=discussion, )[a-z]+(?= hour)",
              "Studio": "(?<=Studio, )[a-z]+(?= hour)"
              }


class Parser:
    """
        Parses UCLA's undergraduate major information. Generates a dictionary of majors and their abbreviations.

    """
    def __init__(self):
        """Generates a dictionary consisting of all UCLA undergraduate majors and their abbreviations"""
        with open("Majors.txt", "r") as myfile:
            text = myfile.readlines()

        self.majors = {}

        for line in text:
            name = re.search("(?<=\t)[A-Z][a-z]+"
                             "(( and| of| in| as a| \|| the|, Study of)*"
                             "( |(\/)|-|, )[A-Z][a-z,]+)*"
                             "( \(undergraduate\))*"
                             "( \(Graduate\))*"
                             "( \(pre-16F\))*"
                             "( \(pre-15F\))*"
                             "(?=\t|  )", line)
            abbrev = re.search("(?<=\t)([A-Z -\/&])+(?=(\t| )"
                               "(AA|DN|EI|EN|GS|HU|IS|LF|LW|MG|MN|MU|NS|PA|PH|PS|SM|SS|TF)\t)", line)
            if name and abbrev:
                self.majors.update({name.group(0).lower(): abbrev.group(0)})

        self.majors.update({"religion, study of": "RELIGN", "neuroscience": "NEUROSC",
                           "mechanical and aerospace engineering": "MECH&AE"})

    def convert_symbol(self, string):
        """Returns the input string with & converted to %26"""
        for i in range(len(string)):
            if string[i] == "&":
                return string[0:i] + "%26" + string[i + 1:]
        return string

    def major_abbrev(self, major, conv_symbol=True):
        """Converts input to major abbreviation, returns the result of conversion"""
        output = ""
        if major.upper() in self.majors.values():
            if conv_symbol:
                output = self.convert_symbol(major.upper())
            else:
                output = major.upper()

        elif major.lower() in self.majors.keys():
            if conv_symbol:
                output = self.convert_symbol(self.majors[major.lower()])
            else:
                output = self.majors[major.lower()]

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
        self.course_list = []

        for course in courses_html:
            course_dict = {"Area": self.major_abbrev(major, conv_symbol=False),
                           "Number": "",
                           "Name": "",
                           "Units": "",
                           "Seminar": 0,
                           "Lecture": 0,
                           "Outside study": 0,
                           "Laboratory": 0,
                           "Discussion": 0,
                           "Studio": 0,
                           "Description": ""
                           }

            for key, value in regex_dict.items():
                if re.search(value, course.get_text()):
                    if re.search(value, course.get_text()).group(0) in num2word:
                        course_dict.update({key: num2word[re.search(value, course.get_text()).group(0)]})
                    else:
                        course_dict.update({key: re.search(value, course.get_text()).group(0)})

            if re.search("(?<=Lecture\/demonstration, )[a-z]+(?= hour)", course.get_text()):
                course_dict.update({"Lecture": num2word[re.search("(?<=Lecture\/demonstration, )[a-z]+(?= hour)",
                                                                  course.get_text()).group(0)]})

            self.course_list.append(course_dict)

        # print(self.course_list)

    def get_course(self, input_key, input_value):
        "Returns a list of courses matching the user's input key and value"
        course_match = []
        for course in self.course_list:
            for key in course:
                if key.lower() == input_key.lower() and re.search(str(input_value).lower(), str(course[key]).lower()):
                    course_match.append(course)
        return course_match



parser = Parser()
parser.parse_courses("bioengineering")
print(parser.get_course("Units", "5"))
