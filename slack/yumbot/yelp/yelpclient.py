import requests
from urllib import quote
from urllib import urlencode

BASE_URL = 'https://api.yelp.com'
TRANSACTION_SEARCH_PATH = '/v3/transactions/delivery/search/'
BUSINESS_SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

class YelpClient(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _obtain_bearer_token(self, host, path):
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        assert self.client_id, 'Please supply your client_id'
        assert self.client_secret, 'Please supply your client_secret'
        data = urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_id,
            'grant_type': GRANT_TYPE,
        })
        headers = {
            'Content-Type': 'application/x-form-urlencoded',
        }

        response = requests.request('POST', url, data=data, headers=headers)
        bearer_token = response.json()['access_token']
        return bearer_token

    def _get_request(self, host, path, bearer_token, url_params=None):
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % bearer_token,
        }

        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()

