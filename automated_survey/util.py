import json
from automated_survey.models import Survey, Question


class SurveyLoader(object):

    def __init__(self, survey_content):
        self.survey = json.loads(survey_content)

    def load_survey(self):
        new_survey = Survey(title=self.survey['title'])
        questions = [Question(body=question['body']
                              # ,kind=question['kind']
                              )
                     for question in self.survey['questions']]
        new_survey.save()
        new_survey.question_set.add(*questions)


def BMIConverter(height,weight):
    #extract height
    extract_height_feet = height.split("'")
    extract_height_inches = extract_height_feet[1].split('"')
    extracted_height_pair = [extract_height_feet[0], extract_height_inches[0]]

    #convert extracted height into meters
    inches_percent_of_foot = float(extracted_height_pair[1]) / 12
    total_height_in_feet = float(extracted_height_pair[0]) + inches_percent_of_foot
    total_height_in_metric = total_height_in_feet * .3048

    #convert extracted weight to kilograms
    total_weight_in_metric = float(weight) *.453592
    return (total_weight_in_metric/total_height_in_metric)/total_height_in_metric
