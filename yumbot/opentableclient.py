import requests
import json
from urllib import quote

BASE_URL = 'https://opentable.herokuapp.com/api'
RESTAURANT_PATH = '/restaurants'

class OpenTableClient(object):

    # Private helper function to send HTTP requests
    def _get_request(self, path, url_params=None):
        url_params = url_params or {}
        url = '{0}{1}'.format(BASE_URL, quote(path.encode('utf8')))

        print('Making request to: ' + url)
        response = requests.get(url, params=url_params)
        return response.json()

    def _search_restaurant(self, name, **kwargs):
        print('Searching OpenTable for restaurants')
        url_params = {
            'name': name
        }

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                url_params[key] = value

        print('Optional params: ' + str(url_params))

        response = self._get_request(RESTAURANT_PATH, url_params)
        print(json.dumps(response))
        return response['businesses']


    def search_restaurant(self, name, **kwargs):
        return self._search_restaurants(name, **kwargs)
