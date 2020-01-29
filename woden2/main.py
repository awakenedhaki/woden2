import click

from gscholar.gscholar import GoogleScholar
from wos.wos import WebOfScience

@click.group(name='woden2')
def main():
    pass

@main.command()
def gscholar():
    pass

@main.command()
def wos():
    pass

if __name__ == "__main__":
    webos = WebOfScience()

    webos.select_search_field('Title')