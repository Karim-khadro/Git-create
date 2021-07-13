from PyInquirer import prompt
from dotenv import load_dotenv
from commandStyle import style
from colorama import Fore, Back, Style, init

from QuestionValidators import GitIgnoreValidator,profileNameValidator

import os
import json
from requests.api import head

load_dotenv()

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

