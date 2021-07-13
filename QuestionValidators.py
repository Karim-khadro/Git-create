from PyInquirer import Validator, ValidationError,prompt
import os
import requests


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
                    message='Please enter a valide language name. To see all valide names: https://api.github.com/gitignore/templates',
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


class LicenseValidator(Validator):
    def validate(self, document):
        if document.text != "":
            licenseUrl = os.getenv("URLLICENSE")
            license = document.text
            license = license.lower()

            licenseUrl = licenseUrl + license
            r = requests.get(licenseUrl)
            if r.status_code == 404:
                raise ValidationError(
                    message='Please enter a valide license key. To see all valide kays: https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/licensing-a-repository#searching-github-by-license-type',
                    cursor_position=len(document.text))  # Move cursor to end




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
            'type': 'input',
            'name': 'license',
            'message': 'Which license? Empty: no license',
            'validate': LicenseValidator,
            'when': lambda answers: answers.get('gitignore', True)
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