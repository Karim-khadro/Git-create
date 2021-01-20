
from __future__ import print_function, unicode_literals
import os
from pprint import pprint
from PyInquirer import Validator, ValidationError, style_from_dict, Token, prompt, print_json, Separator

#* Printing style for the questions
style = style_from_dict({
    Token.Separator: '#00FF00',
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',

})

#*  Check:
#*      If the git ignore file exists in the templates
#*      That only one gitignore file selected
class GitIgnoreValidator(Validator):
    def validate(self, document):
        l = []
        pathTemplate = os.path.join(os.getcwd(), "Gitignore_Template")
        for file in os.listdir(pathTemplate):
            if file.lower().startswith(document.text.lower()):
                l.append(file)
        if document.text == "":
            raise ValidationError(
                message='Please enter some letters to see the propositions',
                cursor_position=len(document.text))  # Move cursor to end
        elif len(l) > 1 or len(l) == 0:
            raise ValidationError(
                message=f'Please enter more letters. Some suggestions : {l[0:5]}',
                cursor_position=len(document.text))  # Move cursor to end


def pretty_print(CL_output):
    leng = len(CL_output)
    if len(CL_output) > 5:
        leng = 4
    columns = leng//200+10
    lines = ("".join(s.ljust(len(s) + 2)
                     for s in CL_output[i:i+columns-1]) + CL_output[i:i+columns][-1] for i in range(0, leng, columns))
    return "".join(lines)

questions = [
    {
        'type': 'confirm',
        'name': 'private',
        'message': 'Private repo?[default value: NO]',
        'default': False
    },
    {
        'type': 'confirm',
        'name': 'issues',
        'message': 'Allows issues?[default value: NO]',
        'default': False
    },
    {
        'type': 'confirm',
        'name': 'wiki',
        'message': 'Has wiki?[default value: NO]',
        'default': False
    },
    {
        'type': 'confirm',
        'name': 'gitignore',
        'message': 'Add git ignore template?[default value: NO]',
        'default': False
    },
    {
        'type': 'input',
        'name': 'gitignoreLanguage',
        'message': 'Which language?',
        'validate': GitIgnoreValidator,
        'when': lambda answers: answers.get('gitignore', True)
    }
]
answers = prompt(questions, style=style)

#* Put the full name of git ignore template
if answers["gitignore"]:
    pathTemplate = os.path.join(os.getcwd(), "Gitignore_Template")
    for file in os.listdir(pathTemplate):
        if file.lower().startswith(answers["gitignoreLanguage"].lower()):
            answers["gitignoreLanguage"] = file

print('Order receipt:')
pprint(answers)
