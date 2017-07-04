import json
import os
from opentableclient import OpenTableClient
from yelpclient import YelpClient

def _attachment(title, attachmentUrl, subtitle):
    attachment = {
        "title": title,
        "subTitle": subtitle,
        "attachmentLinkUrl": attachmentUrl
    }

    return attachment

def _response_card(attachments):
    return {
        "version": 1,
        "contentType": "application/vnd.amazonaws.card.generic",
        "genericAttachments": attachments
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

    if attachments:
        dialog_action['responseCard'] = _response_card(*attachments)

    return dialog_action

def _response(type, fulfillment_state, message, *attachments, **kwargs):
    return {
        "sessionAttributes": _session_attributes(**kwargs),
        "dialogAction": _dialog_action(type, fulfillment_state, message, *attachments)
    }

def _dispatch_event(event):
    opentable = OpenTableClient()
    yelp = YelpClient(os.environ.get('YELP_CLIENT_ID'),
                      os.environ.get('YELP_CLIENT_SECRET'))

    name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    if name == 'SearchRestaurant':
        category = slots['Category'].replace(' ', ',').replace(',', '+').replace('++', '+').lower()
        location = slots['slots']['Location'].replace(' ', ',').replace(',', '+').replace('++', '+')

        resp = yelp.search_restaurants(location, categories=category)

        attachments = []
        for business in resp:
            subtitle = ' '.join(business['location']['display_address'])
            attachments.append(_attachment(business['name'],
                                           business['url'],
                                           subtitle))

        response = _response('Close', 'Fulfilled', 'Search results:', attachments,
                             category=category, location=location)
        print(json.dumps(response))
        return response
    elif name == 'BookRestaurant':
        restaurant = slots['Restaurant'].replace(' ', '+')
        response = _response('Close', 'Fulfilled', 'Reservation created!')
        location = event['currentIntent']['sessionAttributes']['location']
        resp = opentable.search_restaurant(restaurant, )

        return response

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    return _dispatch_event(event)

if __name__ == '__main__':
    l = lambda_handler({
"currentIntent": {
"slots": {
"Category": "chinese",
"Location": "columbia"
},
"name": "SearchRestaurant",
"confirmationStatus": "None"
},
"bot": {
"alias": "",
"version": "$LATEST",
"name": "YumBot"
},
"userId": "w4adpjmomxafuwj7un9ta1vhozbfujuh",
"inputTranscript": "columbia",
"invocationSource": "FulfillmentCodeHook",
"outputDialogMode": "Text",
"messageVersion": "1.0",
"sessionAttributes": ""
}, None)
    print(l)