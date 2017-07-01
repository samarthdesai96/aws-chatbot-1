import json

def response_card(attachments):
    return {
        "responseCard": {
            "contentType": "application/vnd.amazonaws.card.generic",
            "genericAttachments": attachments
        }
    }

def session_attributes(**kwargs):
    return kwargs

def dialog_action(type, fulfillment_state, message, *attachments):
    dialog_action = {
        "type": type,
        "fulfillmentState": fulfillment_state,
        "message": {
            "contentType": "PlainText",
            "content": message
        }
    }

    if attachments is not None:
        dialog_action['responseCard'] = response_card(attachments)

def response(type, fulfillment_state, message, **kwargs):
    return {
        "sessionAttributes": session_attributes(**kwargs),
        "dialogAction": dialog_action(type, fulfillment_state, message)
    }

def dispatch_event(event):
    name = event['currentIntent']['name']
    if name == 'SearchRestaurant':
        category = event['currentIntent']['slots']['Category']
        if category is None:
            return response(None, "Sorry, I couldn't understand that")
        else:
            return response('Close', 'Fulfilled', 'Your category is ' + category, category='chinese')

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    return dispatch_event(event)