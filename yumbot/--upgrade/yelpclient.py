import requests
from urllib import quote
from urllib import urlencode

BASE_URL = 'https://api.yelp.com'
TRANSACTION_SEARCH_PATH = '/v3/transactions/delivery/search/'
BUSINESS_SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
OAUTH_TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

class YelpClient(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    # Private helper function to retrieve the OAuth access_token
    def _obtain_bearer_token(self):
        url = '{0}{1}'.format(BASE_URL, quote(OAUTH_TOKEN_PATH.encode('utf8')))

        assert self.client_id, 'Please supply your client_id'
        assert self.client_secret, 'Please supply your client_secret'

        data = urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': GRANT_TYPE,
        })
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request('POST', url, data=data, headers=headers)
        print('Response: ' + response.content)
        bearer_token = response.json()['access_token']
        return bearer_token

    # Private helper function to send HTTP requests
    def _get_request(self, path, url_params=None):
        url_params = url_params or {}
        url = '{0}{1}'.format(BASE_URL, quote(path.encode('utf8')))

        bearer_token = self._obtain_bearer_token()
        headers = {
            'Authorization': 'Bearer %s' % bearer_token,
        }

        print("Making request to: " + url)
        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()

    def _search_restaurants(self, location, **kwargs):
        print('Searching for restaurants')
        url_params = {
            'term': 'food,restaurants',
            'location': location.replace(' ', '+'),
            'radius': 16093.4, # 10 mile radius in meters
            'limit': 10
        }

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                url_params[key] = value

        print('Optional params: ' + str(url_params))

        response = self._get_request(BUSINESS_SEARCH_PATH, url_params)
        return response['businesses']

    def get_business(self, business_id):
        path = BUSINESS_PATH + business_id

        print("Searching for business: " + business_id)
        response = self._get_request(path)
        return response

    def search_restaurants(self, location, **kwargs):
        return self._search_restaurants(location, **kwargs)
