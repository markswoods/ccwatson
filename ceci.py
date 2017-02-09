from watson_developer_cloud import ConversationV1
import json
import requests
from requests.auth import HTTPBasicAuth

conversation = ConversationV1(
    username='07a61859-9e58-4ca9-9008-3f1fef38e269',
    password='6qpdxCkHE3Py',
    version='2016-09-20'
)

context = {}
workspace_id = '59685873-ce62-47b6-adbf-7e2de15f6ca8'   # Ceci workspace

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
        print 'input: ' + response['input']['text']
        # print 'output: ' + json.dumps(response['output'], indent=2)
        if 'action' in response['output']:
            print 'action: ' + response['output']['action']
    
intent = ''
# Start the conversation
response = conversation.message(
    workspace_id = workspace_id,
    message_input = {'text' : ''},
    context = {}
)
# establish an ongoing context for the conversation
context = response['context']
debug(response)

if len(response['output']['text']) > 0:
    print 'Ceci: ' + response['output']['text'][0]

# Keep the conversation going until a Goodbye intent is received
while intent != 'Goodbye':
    text = raw_input(': ')
    response = conversation.message(
        workspace_id = workspace_id,
        message_input = {'text' : text},
        context = context
    )

    # TODO: Do I need to keep this section?
    # I could extract the Intent and use that as a Resource in the request
    if len(response['intents']) > 0:
        intent = response['intents'][0]['intent']
        context = response['context']
    else:
        intent = ''
    debug(response, verbose=True)

    # Set up a default response based on what the NLP engine provided
    if len(response['output']['text']) > 0:
        response_msg = response['output']['text'][0]
    else:
        response_msg = ''
    
    # Call the Intent Processor, passing everything that came from Watson
 
    print 'Moe: ' + response_msg
