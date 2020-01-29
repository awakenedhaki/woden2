import re

from bibtexparser import loads
from requests.utils import quote
from pprint import pformat
from utils import integer_setter

class Publication(object):
    _BIBTEX = '/scholar?q=info:%s:scholar.google.com/&output=cite&scirp=0&hl=en'

    def __init__(self, src):
        self.title = src.find('a', class_='gsc_a_at').get_text()
        self.citations = integer_setter(src.find('td', class_='gsc_a_c').get_text().replace('*', ''))
        self.year = integer_setter(src.find('td', class_='gsc_a_y').get_text())

        self.author = None
        self.journal = None
        self.volume = None
        self.issue = None
        self.pages = None
        self.publisher = None

    def profiler(self, gscholar):
        query = self._BIBTEX % quote(self.title)
        src = gscholar._search(query)

        print(src)
        bibtex = src.find('a', class_='gs_citi')['href']
        with gscholar._SESSION.get(bibtex, headers=gscholar._headers()) as r:
            citation = loads(r.content).entries[0]

        citation['issue'] = citation['number']

        del citation['number']
        del citation['ID']
        del citation['ENTRYTYPE']

        for k, v in citation.items():
            setattr(self, k, v)

    def to_dict(self):
        return vars(self)

    def __repr__(self):
        return pformat(vars(self))