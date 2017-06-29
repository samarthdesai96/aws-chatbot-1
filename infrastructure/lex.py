#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError

categories = set(line.strip() for line in open('categories.txt'))
categories = [{'value': category.strip()} for category in categories]
'''
'I want to book a reservation',
'Make a reservation for me',
'Make a reservation',
'I would like to book a reservation',
'Book me a reservation at a restaurant',
'I want to book a reservation at {RestaurantName}',
'I would like to book a reservation at {RestaurantName}',
'Book me a reservation at a restaurant at {RestaurantName}',
'''
#AMAZON.FoodEstablishment

lex = boto3.client('lex-models', 'us-east-1')

def fulfillment_activity(type, uri):
    return {
        'type': type,
        'codeHook': {
            'uri': uri,
            'messageVersion': '1.0'
        }
    }

def intent_slot(name, description, slot_constraint, slot_type_version, messages, attempts, priority):
    return [
        {
            'name': name,
            'description': description,
            'slotConstraint': slot_constraint,
            'slotType': name,
            'slotTypeVersion': slot_type_version,
            'valueElicitationPrompt': {
                'messages': messages,
                'maxAttempts': attempts
            },
            'priority': priority
        }
    ]

checksum = ''
try:
    response = lex.put_slot_type(
        name='Category',
        description='Category of restaurant to search for',
        enumerationValues=categories
    )
    checksum = response['checksum']
    print('Successfully put slot type')
except ClientError as e:
    if e.response['Error']['Code'] == 'PreconditionFailedException':
        print('Updating Lex slot')
        response = lex.put_slot_type(
            name='Category',
            description='Category of restaurant to search for',
            enumerationValues=categories,
            checksum=checksum
        )
        print response
    else:
        print(e.response['Error']['Message'])

try:
    response = lex.put_intent(
        name='SearchRestaurant',
        description='Search for restaurants',
        slots=[
            {
                'name': 'Category',
                'description': '',
                'slotConstraint': 'Required',
                'slotType': 'Category',
                'slotTypeVersion': '1',
                'valueElicitationPrompt': {
                    'messages': [
                        {
                            'contentType': 'PlainText',
                            'content': 'What type of restaurant should I search for you?'
                        },
                    ],
                    'maxAttempts': 2
                },
                'priority': 1
            }
        ],
        sampleUtterances=[
            'Search for {Category}',
            'Search for restaurants',
            'Find me a restaurant',
            'Find me a {Category} restaurant'
        ],
        fulfillmentActivity={
            'type': 'CodeHook',
            'codeHook': {
                'uri': 'arn of lambda',
                'messageVersion': '1.0'
            }
        }
    )
    checksum = response['checksum']
except ClientError as e:
    if e.response['Error']['Code'] == 'PreconditionFailedException':
        response = lex.put_intent(
            name='SearchRestaurant',
            description='Search for restaurants',
            slots=[
                {
                    'name': 'Category',
                    'description': '',
                    'slotConstraint': 'Required',
                    'slotType': 'Category',
                    'slotTypeVersion': '1',
                    'valueElicitationPrompt': {
                        'messages': [
                            {
                                'contentType': 'PlainText',
                                'content': 'What type of restaurant should I search for you?'
                            },
                        ],
                        'maxAttempts': 2
                    },
                    'priority': 1
                }
            ],
            sampleUtterances=[
                'Search for {Category}',
                'Search for restaurants',
                'Find me a restaurant',
                'Find me a {Category} restaurant'
            ],
            fulfillmentActivity={
                'type': 'CodeHook',
                'codeHook': {
                    'uri': 'arn of lambda',
                    'messageVersion': '1.0'
                }
            },
            checksum=checksum
        )
    else:
        print(e.response['Error']['Message'])
