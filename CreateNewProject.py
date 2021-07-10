from __future__ import print_function, unicode_literals
from PyInquirer import Validator, ValidationError, style_from_dict, Token, prompt, print_json, Separator
from dotenv import load_dotenv

import sys
import os
import requests
import json

from requests.api import head

load_dotenv()

# TODO : Comments and ReadME
# TODO : Fast mode
# TODO : Add to windows
# TODO : Save profile
# TODO : Add help
# TODO : TESTING


# * Printing style for the questions
style = style_from_dict({
    Token.Separator: '#00FF00',
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',

})

# *  Check:
# *      If the git ignore file exists in the templates
# *      That only one gitignore file selected

class GitIgnoreValidator(Validator):
    def validate(self, document):
        if document.text != "":
            gitignoreUrl = os.getenv("URLGITIGNORE")
            language = document.text
            language = language.lower()
            language = language[0].upper() + language[1:]

            gitignoreUrl = gitignoreUrl + language
            r = requests.get(gitignoreUrl)
            if r.status_code == 404:
                raise ValidationError(
                    message='Please enter a valide language name. To see all valide names: https://api.github.com/gitignore/templates ',
                    cursor_position=len(document.text))  # Move cursor to end
        

folderName = str(sys.argv[1])

questions = [
    {
        'type': 'confirm',
        'name': 'private',
        'message': 'Private repo?[default value: NO]',
        'default': False
    },
    {
        'type': 'confirm',
        'name': 'readme',
        'message': 'Add ReadMe.md?[default value: Yes]',
        'default': True
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
        'message': 'Which language? Empty: no gitignore',
        'validate': GitIgnoreValidator,
        'when': lambda answers: answers.get('gitignore', True)
    }
    # ,{
    #     'type': 'list',
    #     'name': 'gitMethod',
    #     'message': 'Which method?[default value : clone',
    #     'choices': ['Clone', 'Remote'],
    #     'filter': lambda val: val.lower()
    # },
    # {
    #     'type': 'input',
    #     'name': 'remoteName',
    #     'message': 'Remote name?[defalut value : main]',
    #     'default': 'main',
    #     'when': lambda answers: answers.get('gitMethod') == 'remote'
    # }
]
answers = prompt(questions, style=style)

# Create repo on github
token = os.getenv("TOKEN")
query_url = os.getenv("URL")
homePage = os.getenv("HOMEPAGE")
headers = {'Authorization': f'token {token}'}
# if answers["gitMethod"] == "clone":
if answers["gitignore"] and answers["gitignoreLanguage"] != "":
    language = answers["gitignoreLanguage"]
    language = language.lower()
    language = language[0].upper() + language[1:]
    data = {
        "name": folderName,
        "homepage": homePage,
        "private": answers["private"],
        "has_issues": answers["issues"],
        "has_wiki": answers["wiki"],
        "gitignore_template": language,
        "auto_init": answers["readme"]
    }

else:
    data = {
        "name": folderName,
        "homepage": homePage,
        "private": answers["private"],
        "has_issues": answers["issues"],
        "has_wiki": answers["wiki"],
        "gitignore_template": False,
        "auto_init": answers["readme"]
    }

r = requests.post(query_url, headers=headers, data=json.dumps(data))
rsp = r.json()
print(rsp)
git_url = rsp["clone_url"]
commands = [f'git clone {git_url}']
for c in commands:
    os.system(c)

# else:
#     data = {
#         "name": folderName,
#         "homepage": homePage,
#         "private": answers["private"],
#         "has_issues": answers["issues"],
#         "has_wiki": answers["wiki"]
#     }

#     r = requests.post(query_url, headers=headers, data=json.dumps(data))
#     rsp = r.json()
#     print(rsp)
#     git_url = rsp["clone_url"]
#     os.mkdir(folderName)
#     os.chdir(folderName)
#     commands = [
#                 'git init',
#                 f'git remote add origin {git_url}',
#                 'git add .',
#                 'git commit -m "Initial commit"',
#                 f'git push -u origin {answers["remoteName"]}']
#     if answers["readme"]:
#         commands.insert(0,f'echo "# {folderName}" >> README.md')
#     if answers["gitignore"]:
#         url = str(os.getenv("URLGITIGNOR"))+str(answers["gitignoreLanguage"]).split(".gitignore")[0]
#         print(url)
#         rget = requests.get(url)
#         rsp = rget.json()
#         open(".gitignore", 'wb').write(bytes(rsp["source"],encoding='utf8'))

#     print(commands)
#     for c in commands:
#         os.system(c)
