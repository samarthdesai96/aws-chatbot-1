#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError

lex = boto3.client('lex-models', 'us-east-1')
search_utterances = [
    'Search for {Category} restaurants in {Location}',
    'Find {Category} restaurants in {Location}',
    'Search for restaurants',
    'Find me a restaurant in {Location}',
    'Find a {Category} restaurant',
    'Search for a {Category} restaurant',
    'Look up a {Category} restaurant',
    'Find me a {Category} restaurant in {Location}'
]
reservation_utterances = [
    'Make a reservation for me',
    'I want to book a reservation at {Restaurant}',
    'I would like to book a reservation at {Restaurant}',
    'Book me a reservation at a restaurant at {Restaurant}'
]

def _slot_message(messages):
    slot_messages = []
    for message in messages:
        slot_messages.append({
            'contentType': 'PlainText',
            'content': message
        })
    return slot_messages

def _intent_slot(name, slot_constraint, slot_type, messages, *version):
    slot = {
        'name': name,
        'slotConstraint': slot_constraint,
        'slotType': slot_type,
        'valueElicitationPrompt': {
            'messages': messages,
            'maxAttempts': 2
        },
        'priority': 1
    }

    if version:
        slot['slotTypeVersion'] = version[0]

    return slot

def _put_slot_type(slot_name, enum_values):
    checksum = ''
    try:
        response = lex.put_slot_type(
            name=slot_name,
            enumerationValues=enum_values
        )
        checksum = response['checksum']
        print('Successfully put slot type')
    except ClientError as e:
        if e.response['Error']['Code'] == 'PreconditionFailedException':
            print('Updating Lex slot')
            response = lex.put_slot_type(
                name=slot_name,
                enumerationValues=enum_values,
                checksum=checksum
            )
            print(response['ResponseMetadata']['HTTPStatusCode'])
        else:
            print(e.response['Error']['Message'])

def _put_intent(intent_name, slots, sample_utterances):
    checksum = ''
    try:
        print("Creating intent")
        response = lex.put_intent(
            name=intent_name,
            slots=slots,
            sampleUtterances=sample_utterances,
            fulfillmentActivity={
                'type': 'CodeHook',
                'codeHook': {
                    'uri': 'arn:aws:lambda:us-east-1:729905221641:function:aws-chatbot-lambda',
                    'messageVersion': '1.0'
                }
            }
        )
        checksum = response['checksum']
    except ClientError as e:
        if e.response['Error']['Code'] == 'PreconditionFailedException':
            print("Updating intent")
            response = lex.put_intent(
                name=intent_name,
                slots=slots,
                sampleUtterances=sample_utterances,
                fulfillmentActivity={
                    'type': 'CodeHook',
                    'codeHook': {
                        'uri': 'arn:aws:lambda:us-east-1:729905221641:function:aws-chatbot-lambda',
                        'messageVersion': '1.0'
                    }
                },
                checksum=checksum
            )
        else:
            print(e.response['Error']['Message'])

def main():
    categories = set(line.strip() for line in open('categories.txt'))
    categories = [{'value': category.strip()} for category in categories]

    search_intent_slots = []
    reservation_intent_slots = []

    _put_slot_type('Category', categories)
    search_intent_slots.append(_intent_slot('Category', 'Required', 'Category',
                                            _slot_message(['What are you in the mood for?']), '$LATEST'))
    search_intent_slots.append(_intent_slot('Location', 'Required', 'AMAZON.US_CITY',
                                            _slot_message(['Where should I search?'])))

    reservation_intent_slots.append(_intent_slot('Restaurant', 'Required', 'AMAZON.FoodEstablishment',
                                                 _slot_message(['Where would you like to make a reservation?'])))

    _put_intent('SearchRestaurant', search_intent_slots, search_utterances)
    _put_intent('BookRestaurant', reservation_intent_slots, reservation_utterances)


if __name__ == '__main__':
    main()

'''     
    name='SearchRestaurant',
    description='Search for restaurants',
    slots=[
        {
            'name': 'Category',
            'description': '',
            'slotConstraint': 'Required',
            'slotType': 'Category',
            'slotTypeVersion': '$LATEST',
            'valueElicitationPrompt': {
                'messages': [
                    {
                        'contentType': 'PlainText',
                        'content': 'What are you in the mood for?'
                    },
                ],
                'maxAttempts': 2
            },
            'priority': 1
        },
        {
            'name': 'Location',
            'description': '',
            'slotConstraint': 'Required',
            'slotType': 'AMAZON.US_CITY',
            'valueElicitationPrompt': {
                'messages': [
                    {
                        'contentType': 'PlainText',
                        'content': 'Where should I search?'
                    },
                ],
                'maxAttempts': 2
            },
            'priority': 1
        }
    ],
    sampleUtterances=[
        'Search for {Category} restaurants in {Location}',
        'Find {Category} restaurants in {Location}',
        'Search for restaurants',
        'Find me a restaurant in {Location}',
        'Find a {Location} restaurant',
        'Search for a {Location} restaurant',
        'Look up a {Location} restaurant',
        'Find me a {Category} restaurant in {Location}'
    ],
    fulfillmentActivity={
        'type': 'CodeHook',
        'codeHook': {
            'uri': 'arn:aws:lambda:us-east-1:729905221641:function:aws-chatbot-lambda',
            'messageVersion': '1.0'
        }
    }
)
'''