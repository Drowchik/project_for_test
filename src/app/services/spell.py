
import requests


class SpellChecker:
    def __init__(self) -> None:
        self.api_url = "https://speller.yandex.net/services/spellservice.json/checkText"

    def check_text(self, text):
        response = requests.post(self.api_url, data={'text': text})
        return response.json()

    def validate_text(self, text):
        errors = self.check_text(text)
        return errors
