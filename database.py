import requests
import csv
import inflection
import discord

from io import StringIO
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Database:
    def __init__(self, url):
        self.url = url
        self.dictionary = {}
        self.refresh_db()


    def refresh_db(self):
        dat = requests.get(self.url)
        dat.encoding = "utf-8"
        csv_file = StringIO(dat.text)
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        self._process_rows(rows)

    
    def _process_rows(self, rows):
        for row in rows:
            self._build_dictionary(row)

    def _build_dictionary(self, row):
        pass