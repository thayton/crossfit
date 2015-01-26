import requests
import traceback

from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class SoupRequestor(object):
    def __init__(self):
        self.validate_url = URLValidator()

    def get(self, url):
        try:
            self.validate_url(url)
        except ValidationError, e:
            print e        
            return (None, None)

        try:
            r = requests.get(url)
        except Exception, err:
            print traceback.format_exc()
            return (None, None)

        s = BeautifulSoup(r.text)
        return (r,s)
