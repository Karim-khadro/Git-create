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