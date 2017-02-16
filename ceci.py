#!/usr/bin/env python
# This is the ceci chat client. I've tried to simplify this one from my
# prior work on barwatson. In this one, we'll extract the Intent returned
# from Watson and forward to the appropriate Intent Processor. 
from watson_developer_cloud import ConversationV1
import json
import requests
import os   # I'm using these to grab the userid, I'll pass this to Watson as part of Context
import pwd  # The Intent Processor will determine if this is an Agent or CCC
import sys, getopt
from requests.auth import HTTPBasicAuth

def debug(response, verbose=False):
    if verbose:
        print json.dumps(response, indent=2) 
    else:  
        if len(response['intents']) > 0:
            print 'intents: ' + response['intents'][0]['intent']
            #for i in response['intents']:
            #    print i
        if len(response['entities']) > 0:
            print 'entities: ' 
            for e in response['entities']: 
                print e
        if response['input']['text'] != '':
            print 'input: ' + response['input']['text']
        # print 'output: ' + json.dumps(response['output'], indent=2)
        if 'action' in response['output']:
            print 'action: ' + response['output']['action']
        print 'Context: %s' % json.dumps(response['context'], indent=2)

#
# Set up
#
conversation = ConversationV1(
    username='07a61859-9e58-4ca9-9008-3f1fef38e269',
    password='6qpdxCkHE3Py',
    version='2016-09-20'
)

workspace_id = '59685873-ce62-47b6-adbf-7e2de15f6ca8'   # Ceci workspace
intent_processor = 'https://mw-ccwatson.herokuapp.com/'

#
# Get command line parms
#
username = pwd.getpwuid(os.getuid()).pw_name    # Default, unless overridden at command line
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hu:', ['help', 'local'])
except getopt.GetoptError:  
    print 'Usage: python ceci.py [-u username]'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-u':
        username = arg
    if opt == '--local':
        intent_processor = 'http://localhost:5000/'
    if opt in ('-h', '--help'):
        print 'Usage: python ceci.py [-u username]'
        sys.exit(2)
    
# Initialize the context with a username, the IP will use this to determine the user type
context = {'username': username}

#    
# Start the conversation with Watson's Welcome
#
response = conversation.message(
    workspace_id = workspace_id,
    message_input = {'text' : ''},
    context = context
)

context = response['context']
intent = 'Welcome'  # No intent established with the Welcome call so we'll override
# debug(response, verbose=True)

# Keep the conversation going until a Goodbye intent is received
while intent != 'Goodbye':    
    # Set up a default response based on what Watson provided
    if len(response['output']['text']) > 0:
        response_msg = response['output']['text'][0]
    else:
        response_msg = ''

    # Call the Intent Processor, passing the context that came from Watson
    ip_response = json.loads(requests.post(intent_processor + intent, json=context, auth=HTTPBasicAuth('mwoods', 'hp92275a')).text)
    if ip_response['message'] != '':
        response_msg = ip_response['message']
        
    context = ip_response['context']    # renew the context
    response['context'] = context       # update the response context (for debugging)

    debug(response)   # debug AFTER Intent Processor has run - one full convo cycle
    
    print 'Ceci: ' + response_msg

    # Get user input and pass to Watson Conversation Service, preserving context
    text = raw_input(': ')
    response = conversation.message(
        workspace_id = workspace_id,
        message_input = {'text' : text},
        context = context
    )

    context = response['context']   # extract context so I can pass it to the Intent Processor
    if len(response['intents']) > 0:
        intent = response['intents'][0]['intent']
    else:
        intent = '' 

