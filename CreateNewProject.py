from __future__ import print_function, unicode_literals
from dotenv import load_dotenv
from colorama import Fore, Style, init
from profilesManager import manageProfiles
from QuestionValidators import questions
from PyInquirer import  prompt
from commandStyle import style
import sys
import os
import requests
import json
import argparse

load_dotenv()
init()

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

# * CMD arguments 
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
            "license_template": answers["license"],
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
            "license_template": answers["license"],
            "gitignore_template": False,
            "auto_init": answers["readme"]
        }

    # * Create repo on github
    r = requests.post(query_url, headers=headers, data=json.dumps(data))
    rsp = r.json()
    git_url = rsp["clone_url"]

    # * Create local repo
    commands = [f'git clone {git_url}']
    for c in commands:
        os.system(c)
