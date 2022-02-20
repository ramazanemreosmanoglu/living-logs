#! /usr/bin/python
import click
from config import Config
from LogJournal import LogJournal
from Log import Log
from datetime import datetime
import os

conf = Config()
journal = LogJournal(conf.config)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('file', type=click.File('w'))
def create_journal(file):
    """Creates a new journal and adds it to the config."""

    conf.config['journal_file'] = os.path.abspath(file.name)
    conf.save()
    click.echo("Created a new journal.")


@cli.command()
@click.argument('file', type=click.File('r'))
def set_default_journal(file):
    """
    Sets the default journal.
    """

    conf.config['journal_file'] = os.path.abspath(file.name)
    conf.save()
    click.echo("Default journal has been changed.")

@cli.command()
def get_todays_logs():
    """Returns todays logs."""
    ...


@cli.command()
@click.argument('text', nargs=-1, type=click.STRING)
def insert(text):
    """Insert log."""

    log = Log(' '.join(text), datetime.now())
    journal.logs += [log]

@cli.command()
@click.argument('format', nargs=1, type=click.STRING)
def set_date_format(format):
    """
    Change date format.
    """


if __name__ == "__main__":
    cli()
