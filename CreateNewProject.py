from __future__ import print_function, unicode_literals
from logging import fatal
from PyInquirer import Validator, ValidationError, prompt
from dotenv import load_dotenv
from commandStyle import style
from colorama import Fore, Back, Style, init

import ast
import sys
import os
import requests
import json
import argparse
from requests.api import head

load_dotenv()
init()
# TODO : Comments and ReadME
# TODO : use the new profiles system in creating    
# TODO : Clean code
# TODO : Add help
# TODO : read path from .env in bat


# *  Question validator:
# *      If the git ignore file exists in the templates
# *      By sending request to the api

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


class profileNameValidator(Validator):
    def validate(self, document):
        # * Check if empty or already used
        if document.text == "":
            raise ValidationError(
                message='Please enter a name. This field can\'t be empty',
                cursor_position=len(document.text))  # Move cursor to end
        pf = os.getenv("PROFILES_STORAGE")
        if os.path.exists(os.path.join(pf, document.text+".txt")):
            raise ValidationError(
                message='The profile already exists. Please choose another name',
                cursor_position=len(document.text))  # Move cursor to end


# Questions to ask

# * Profiles managment
def createProfile():
    profileQuestions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'Profile name?',
            'validate': profileNameValidator
        },
        {
            'type': 'confirm',
            'name': 'private',
            'message': 'Private repo?',
            'default': ""
        },
        {
            'type': 'confirm',
            'name': 'readme',
            'message': 'Add ReadMe.md?',
            'default': ""
        },
        {
            'type': 'confirm',
            'name': 'issues',
            'message': 'Allows issues?',
            'default': ""
        },
        {
            'type': 'confirm',
            'name': 'wiki',
            'message': 'Has wiki?',
            'default': ""
        },
        {
            'type': 'confirm',
            'name': 'gitignore',
            'message': 'Add git ignore template?[default value: NO]',
            'default': ""
        },
        {
            'type': 'input',
            'name': 'gitignoreLanguage',
            'message': 'Which language? Empty: no gitignore',
            'validate': GitIgnoreValidator,
            'when': lambda answers: answers.get('gitignore', True)
        }
    ]
    print("Creating new profile...\n")
    print(Fore.CYAN + 'NOTES: -if the answer is empty the question will be asked when using the profile\n       -if wrong answer, the answer will be empty')
    print(Style.RESET_ALL)

    answers = prompt(profileQuestions, style=style)

    # * Recap of the answers
    print(Fore.CYAN +
          f'\n-------------------------\n {answers["name"]} progfile recap:\n {answers}\n-------------------------\n')
    print(Style.RESET_ALL)

    # * Save to file
    if answers != {}:
        pf = os.getenv("PROFILES_STORAGE")
        profiles = {}

        # * Read the profiles to check if the name already exists
        with open(pf, 'r') as f:
            profiles = json.load(f)
            # profiles = jasonFile["profiles"]
            f.close()

        for p in profiles["profiles"]:
            if p["name"] == answers["name"]:
                print(Fore.RED + 'This profile name already exists')
                print(Style.RESET_ALL)
                exit(0)

        # * Savet the new profile
        profiles["profiles"].append(answers)
        with open(pf, 'w') as f:
            f.seek(0)
            json.dump(profiles, f, indent=4)
            f.close()

    print(Fore.GREEN + f'Profile created')
    print(Style.RESET_ALL)


def listProfiles():
    pf = os.getenv("PROFILES_STORAGE")
    # * Read the profiles to check if the name already exists
    profiles = {}
    with open(pf, 'r') as f:
        profiles = json.load(f)
        f.close()

    if len(profiles["profiles"]) < 1:
        print(Fore.RED+'No profiles created')
        print(Style.RESET_ALL)
    else:
        print("\n")
        for p in profiles["profiles"]:
            print(Fore.YELLOW + f'{p}\n')
            print(Style.RESET_ALL)

    
def deleteProfile(profile):
    pf = os.getenv("PROFILES_STORAGE")
    # * Read the profiles to check if the name already exists
    profiles = {}
    with open(pf, 'r') as f:
        profiles = json.load(f)
        f.close()

    deleted = False
    for i in range(len(profiles["profiles"])):
        if profiles["profiles"][i]["name"] == profile:
            profiles["profiles"].pop(i)
            deleted = True
            break
    if deleted:
        with open(pf, 'w') as f:
            f.seek(0)
            json.dump(profiles, f, indent=4)
            f.close()
        print(Fore.YELLOW+f'Profile deleted')
        print(Style.RESET_ALL)

    else:
        print(Fore.YELLOW+f'The profile dosen\'t exist ')
        print(Style.RESET_ALL)
    

def manageProfiles():
    l = ["Create", "list", "Delete", "Cancel"]
    while True:
        profileQuestions = [
            {
                'type': 'rawlist',
                'name': 'choice',
                'message': 'Choose the action:',
                'choices': l
            }
        ]
        answers = prompt(profileQuestions, style=style)
        if answers['choice'] == l[0]:
            createProfile()

        elif answers['choice'] == l[1]:
            listProfiles()

        elif answers['choice'] == l[2]:
            question = [
                {
                    'type': 'input',
                    'name': 'pdelete',
                    'message': 'Enter the profile name to delete ? (empty to cancel)'
                }
            ]
            answer = prompt(question, style=style)
            if answer["pdelete"] != "":
                deleteProfile(answer["pdelete"] )
        else:
            exit(0)


def chekRepoName(rName):
    if os.path.exists(rName):
        print(Fore.RED + "Error: repo name already exist on LOCAL")
        print(Style.RESET_ALL)
        exit(0)
    token = os.getenv("TOKEN")
    query_url = os.getenv("URL")
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers)
    rsp = r.json()

    for r in rsp:
        if rName == r['name']:
            print(Fore.RED + "Error: repo name already exist on GIT")
            print(Style.RESET_ALL)
            exit(0)


parser = argparse.ArgumentParser()

parser.add_argument(
    "-e", "--edit",
    dest='funcs', action="append_const", const=manageProfiles,
    help="Manage profiles.", )

parser.add_argument(
    "-n", "--new",
    dest='new',
    help="Create new repo (local & github) [repo_name]", type=str)

parser.add_argument(
    "-p", "--profile",
    help="Use a profile params to create the repo [profile_name]")

args = parser.parse_args()

if args.funcs != None:
    for func in args.funcs:
        func()


if args.new:

    #  * Check folder name on git & localy
    folderName = str(sys.argv[2])
    chekRepoName(folderName)

    profileExist = False
    
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
    ]

    # * use a profile
    if args.profile:
        pf = os.getenv("PROFILES_STORAGE")

        # * Read
        profiles = {}
        with open(pf, 'r') as f:
            profiles = json.load(f)
            f.close()
        
        profileAnswers = {} 
        for p in profiles["profiles"]:
            if p["name"] ==args.profile:
                profileExist = True
                profileAnswers = p

        if profileExist == False:
            print(
                Fore.RED + f'The profile dosen\'t exist.(contiune using normal mode)')
            print(Style.RESET_ALL)

        if profileExist:
            # * Complete missing answers
            i = 0
            answers = {}
            qtoAsk = []

            for a in profileAnswers:
                # * remove the profile name
                if a == "name":
                    continue
                # * copy answers to the answers variable
                answers[a] = profileAnswers[a]
                if profileAnswers[a] == "":
                    if a == "gitignoreLanguage" and profileAnswers["gitignore"] == False:
                        continue
                    qtoAsk.append(i)
                i += 1

            if qtoAsk != []:
                missingQ = []
                print(
                    Fore.CYAN + f'Completing missed answers (empty answer in the profile)')
                print(Style.RESET_ALL)
                for q in qtoAsk:
                    missingQ.append(questions[q])

                missingA = prompt(missingQ, style=style)
                # * Merge the 2 answers
                for a in missingA:
                    answers[a] = missingA[a]

            print(Fore.YELLOW + f'\nThe repo will be created with those parameters:')
            print(answers)
            print(Style.RESET_ALL)

    if profileExist == False:
        answers = prompt(questions, style=style)

    # Create repo on github
    token = os.getenv("TOKEN")
    query_url = os.getenv("URL")
    homePage = os.getenv("HOMEPAGE")
    headers = {'Authorization': f'token {token}'}

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
    git_url = rsp["clone_url"]
    commands = [f'git clone {git_url}']
    for c in commands:
        os.system(c)
