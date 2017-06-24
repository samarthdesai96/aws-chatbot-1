import requests
from yelpresponse import YelpResponse
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

    # Private helper function to retrieve the OAuth access_token
    def _obtain_bearer_token(self):
        url = '{0}{1}'.format(BASE_URL, quote(TOKEN_PATH.encode('utf8')))

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

    def get_business(self, business_id):
        path = BUSINESS_PATH + business_id

        print("Searching for business: " + business_id)
        response = self._get_request(path)
        yelp_response = YelpResponse(response['id'], response['name'], response['image_url'],
                                     response['is_closed'], response['url'], response['price'],
                                     response['rating'], response['review_count'], response['phone'],
                                     response['photos'], response['hours'], response['categories'],
                                     response['location'], response['transactions'])
        return yelp_response