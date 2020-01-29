from itertools import chain
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class WebOfScience(object):
    _HOST = 'https://apps.webofknowledge.com'

    # FIND_ELEMENT_BY =========================================================
    _DATABASE = 'database'
    _SEARCH = 'select1'
    _TIMESPAN = 'timespan'
    _INPUT = 'value(input)'
    _EXPORT = 'exportTypeName'

    # SELECTION VALUES ========================================================
    _FIELDS = {
        "TS": "Topic"
        "TI": "Title"
        "AU": "Author"
        "SO": "Publication Name"
        "PY": "Year Published"
        "FO": "Funding Agency"
        "OG": "Organization-Enhanced"
        "ALL": "All Fields"
        "UT": "Accession Number""
        "AD": "Address"
        "AI": "Author Identifiers"
        "CF": "Conference"
        "DT": "Document Type"
        "DO": "DOI"
        "ED": "Editor"
        "FG": "Grant Number"
        "GP": "Group Author"
        "LA": "Language"
        "PMID": "PubMed ID"
    }
    _DATABASES = (
        'All Databases',
        'Web of Science Core Collection',
        'FSTA',
        'KCI-Korean Journal Database',
        'MEDLINE',
        'Russian Science Citation Index',
        'SciELO Citation Index',
        'Zoological Record',
    )
    _TIMESPANS = {
        'ALL': ' All years     (1900 - 2020)       ',
        'Latest5Years': ' Last 5 years        ',
        'YearToDate': ' Year to date        ',
        '4week': ' Last 4 weeks        ',
        '2week': ' Last 2 weeks        ',
        '1week': ' Current week        ',
        'CUSTOM': ' Custom year range        '
    }

    # DUNDERMETHODS ===========================================================

    def __init__(self, driver='chrome', search_type='basic'):
        self._driver = self._select_driver(driver)
        self._driver.get(self._HOST)

        self.name = self._driver.find_element_by_id('customerName').text
        self.id = self._driver.find_element_by_id('customerId').text

    # SEARCH ==================================================================

    def search(self, text, input_box, _return=False):
        box = self._driver.find_element_by_id(input_box)
        box.send_keys(text)

        if _return:
            box.send_keys(Keys.RETURN)

    def search_title(self, title, timespan=None):
        if timespan is not None:
            self.select_timespan(timespan)
        self.select_search_field('Title')
        self.search(title, input_box=self._INPUT, _return=True)

    def search_author(self, text, timespan=None):
        if timespan is not None:
            self.select_timespan(timespan)
        self.select_search_field('Author')
        self.search(title, input_box=self._INPUT, _return=True)

    # SELECTIONS ==============================================================

    def _select(self, option, direct=False, **kwargs):
        tag, attribute = chain(*kwargs.items())
        find = getattr(self._driver, f'find_element_by_{tag}')

        if not direct:
            menu = Select(find(attribute))
        else:
            menu = Select(
                find(attribute).find_element_by_tag_name('select')
            )

        menu.select_by_visible_text(option)

    @validate_option(self._DATABASES)
    def select_database(self, db):
        self._select(id=self._DATABASE,
                     option=db)

    @validate_option(self._FIELDS)
    def select_search_field(self, field):
        self._select(id=self._SEARCH,
                     option=field)

    @validate_option(self._TIMESPANS)
    def select_timespan(self, timespan):
        self._select(option=timespan,
                     direct=True,
                     id=self._TIMESPAN)
                    
    # TOOLS ==================================================================

    def export(self):
        pass

    def sort(self, by):
        pass

    def quit(self):
        self._driver.close()

    @staticmethod
    def _select_driver(driver):
        drivers = {
            'chrome': webdriver.Chrome
        }
        if driver not in drivers:
            raise ValueError()
        return drivers[driver]()