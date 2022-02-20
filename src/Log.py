import re

class Log:
    def __init__(self, text, date):
        self.text = text
        self.date = date
        self.tags = Log.get_tags(text)

    @staticmethod
    def get_tags(text):
        """Returns tags of the text in a list."""

        return re.findall(r'\B@[A-z]+', text)

    def __repr__(self):
        return f"<Log '{self.text}'>"
