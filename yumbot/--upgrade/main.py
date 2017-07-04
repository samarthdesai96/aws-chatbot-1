import json
import os
from yelpclient import YelpClient

def _response_card(attachments):
    return {
        "responseCard": {
            "contentType": "application/vnd.amazonaws.card.generic",
            "genericAttachments": attachments
        }
    }

def _session_attributes(**kwargs):
    return kwargs

def _dialog_action(type, fulfillment_state, message, *attachments):
    dialog_action = {
        "type": type,
        "fulfillmentState": fulfillment_state,
        "message": {
            "contentType": "PlainText",
            "content": message
        }
    }

    if attachments is not None:
        dialog_action['responseCard'] = _response_card(attachments)

def _response(type, fulfillment_state, message, **kwargs):
    return {
        "sessionAttributes": _session_attributes(**kwargs),
        "dialogAction": _dialog_action(type, fulfillment_state, message)
    }

def _dispatch_event(event):
    yelp = YelpClient(os.environ.get('YELP_CLIENT_ID'),
                      os.environ.get('YELP_CLIENT_SECRET'))

    name = event['currentIntent']['name']
    if name == 'SearchRestaurant':
        category = event['currentIntent']['slots']['Category'].replace(',', '+').replace(' ', ',').replace('++', '+')
        location = event['currentIntent']['slots']['City'].replace(',', '+').replace(' ', '+').replace('++', '+')
        resp = yelp.search_restaurants(location, categories=category)
        return _response('Close', 'Fulfilled', 'Your category is ' + category, category='chinese')

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    return _dispatch_event(event)