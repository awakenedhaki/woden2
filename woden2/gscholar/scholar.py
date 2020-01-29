import re

from pprint import pformat
from utils import integer_setter
from .publication import Publication

_ID = re.compile(r'.*citations\?.*user=([A-z1-9_]*).*')

class Scholar(object):
    _PROFILEPUB = '/citations?hl=en&user=%s&cstart=%d&pagesize=100'
    _INCREMENT = 100

    def __init__(self, src, gscholar=None):
        if gscholar is not None:
            self.parser(src, **{
                'keywords': 'gsc_prf_inta gs_ibl',
                'affiliation': 'gs_prf_il',
                'email': 'div.gs_prf_il#gsc_prf_ivh',
            })

            self.name = src.select_one('div#gsc_prf_in').get_text()
            self.id = _ID.match(src.find('link', rel='canonical')['href']).group(1)
            table = src.select_one('table#gsc_rsb_st').find_all('td', class_='gsc_rsb_std')
            ALL_COLUMN = slice(0, -1, 2)
            self.citations, self.h_index, self.i10_index = [
                integer_setter(cell.get_text()) for cell in table[ALL_COLUMN]
            ]
            self.publications = self._search_publications(src, gscholar)
        else:
            self.parser(src, **{
                'id_': 'gs_ai_pho',
                'keywords': 'gs_ai_one_int',
                'affiliation': 'gs_ai_aff',
                'email': 'div.gs_ai_eml'
            })

            self.name = src.find(class_='gs_ai_name').get_text()
            citations = src.find(class_='gs_ai_cby').get_text().replace('Cited by ', '')
            self.citations = integer_setter(citations)

            self.publications = None
            self.h_index = None,
            self.i10_index = None

        self.photo = src.img['src']

    def parser(self, src, keywords, affiliation, email, id_=None):
        self.keywords = [kword.get_text() for kword in src.find_all(class_=keywords)]

        affiliation = src.find(class_=affiliation)
        if affiliation:
            self.affiliation = affiliation.get_text()
        email = src.select_one(email)
        if email:
            self.email = email.get_text().replace('Verified email at', '')

        if id_ is not None:
            self.id = _ID.match(src.find(class_=id_)['href']).group(1)

    def profiler(self, gscholar):
        soup = gscholar.search_profile(self.id)
        self.profile_attrs(soup)
        
    def _search_publications(self, src, gscholar):
        def _publications(src):
            button = src.find('button', id='gsc_bpf_more')
            cstart = self._INCREMENT
            while True:
                for pub in src.find_all('tr', class_='gsc_a_tr'):
                    yield Publication(pub)

                if 'disabled' in button.attrs:
                    break

                query = self._PROFILEPUB % (self.id, cstart)
                src = gscholar._search(query)

                button = src.find('button', id='gsc_bpf_more')
                cstart += self._INCREMENT

        return list(_publications(src))

    def to_dict(self):
        scholar = vars(self)
        scholar['publications'] = [pub.to_dict() for pub in scholar['publications']]
        return scholar

    def __repr__(self):
        repr = vars(self).copy()
        count = 'Not collected' if self.publications is None else len(repr['publications'])
        repr['publications'] = f'[{count} publications]'
        return pformat(repr)