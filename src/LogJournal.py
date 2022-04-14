import os
from Log import Log
import re
import datetime

NEWLINE = "\n"


class ParseError(Exception):
    pass


class LogJournal:
    def __init__(self, config):
        self.config = config
        self._logs = []

    @property
    def logs(self):
        self._load()
        return self._logs

    @logs.setter
    def logs(self, new):
        self._update(new)
        self._logs = new

    def _load(self, filename=None):
        """Load logs from file."""

        filename = filename or self.config['journal_file']

        if not os.path.exists(filename):
            # Create a new file.
            with open(filename, 'w'): # FIXME: FileNotFoundError
                pass

            self._logs = []

        else:
            # Read and parse content.
            with open(filename, 'r') as file:
                self._logs = self._parse(file.read())

    def _parse(self, content):
        """
        Parse given file content as logs.
        """
        content = content.strip(NEWLINE)
        logs = []

        if not content:
            return []

        date_regex = re.compile('^\[.+\]')

        for n, line in enumerate(content.split(NEWLINE), start=1):
            match = date_regex.match(line)
            if match is None:
                raise ParseError(f'Couldn\'t parse line {n}.')

            date_part = match.group()

            # Parse date
            date = datetime.datetime.strptime(date_part, f"[{self.config['dateformat']}]")

            # Parse text
            text = line.lstrip(f"{date_part} ")

            logs.append(
                Log(text, date)
            )

        return logs

    def _update(self, new):
        lines = []

        for log in new:
            lines.append(f"[{log.date.strftime(self.config['dateformat'])}] {log.text}{NEWLINE}")

        with open(self.config['journal_file'], 'w') as f:
            f.writelines(lines)

