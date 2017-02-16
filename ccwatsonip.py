from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_basicauth import BasicAuth
import requests
import json

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'mwoods'
app.config['BASIC_AUTH_PASSWORD'] = 'hp92275a'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
ccwatsonip = Api(app)

wsr_url = 'https://agentsupport.allstate.com/webservices/'
sn_url = 'https://allstatesand2.service-now.com/api/now/table/incident'
sn_user = 'sys_rest_watson'
sn_pwd = '!wNT4jm*$rRs'

def log_incident(ci, description, notes, resolutionCode):
    # create a Service Now incident and return the incident number
    incident_number = '###Error###'
    headers = {'Content-Type':'application/json', 'Accept':'application/json'}
    payload = {}
    payload['userid'] = sn_user
    payload['assignment_group'] = 'Ceci Watson ABO Chat POC'
    payload['caller_id'] = sn_user
    payload['contact_type'] = 'Ceci Watson'
    payload['short_description'] = description
    payload['work_notes'] = notes
    payload['category'] = 'investigation'
    payload['cmdb_ci'] = ci
    payload['incident_state'] = 'resolved'   
    payload['resolution_code'] = resolutionCode
    
    response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=headers, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        print 'Svc Now incident created status code : %d' % response.status_code 
        print 'Incident: %s sys-id: %s' % (response.json()['result']['number'], response.json()['result']['sys_id'])
        incident_number = response.json()['result']['number']
    elif response.status_code == 204:
        # everything worked, but there is no response body from which to get an incident number
        incident_number = 'INC000000'
    else:
        # something went wrong, so record it in the logs
        print 'Svc Now Status: %d' % response.status_code 
        print ('Headers:', response.headers)
        print 'Error Response: ' + json.dumps(response.json(), indent=2)
        
    return incident_number
    
class Welcome(Resource):
    def post(self):
        print 'Handling Welcome intent...'
        context = request.get_json()
        
        # Extract the username and do a lookup to determine if this is an Agent, or CCC
        #print json.dumps(context, indent=2)
        username = context['username']
        if username == 'markswoods':
            type = 'agent'
        else:
            type = 'internal'
        context['type'] = type
        
        #print 'username: %s, type: %s' % (username, type)
        return {'message': '', 'context': context}

class AgencyChangeRequest(Resource):
    def post(self):
        print 'Handling AgencyChangeRequest intent...'
        context = request.get_json()
        
        #print json.dumps(context, indent=2)
        form = 'Internal Agency Change Request'
        msg = 'The required WSR form is available only for P&C policies. ' + \
            'Click ' + wsr_url + ' and select category Agency Change Request to find the ' + ' form.'
        msg += ' Note: For MD and VA you must submit the Agency Change Request PDF to the Call Center.'
            
        incident_number = log_incident('WSR - Web Service Request', 'Intent: Agency Change Request', form, 'Education/Training')
        msg += ' I have created incident #' + incident_number + ' for you in Service Now'
        return {'message': msg, 'context': context}

class Goodbye(Resource):
    def post(self):
        print 'Handling Goodbye...'  
        context = request.get_json()
        return {'message': '', 'context': context}
              
class Auth(Resource):
    def get(self):
        print "Authentication made"
        return {'response': 'Authorized'}
        
# Pure rest
ccwatsonip.add_resource(Welcome, '/Welcome')
ccwatsonip.add_resource(Goodbye, '/Goodbye')
ccwatsonip.add_resource(AgencyChangeRequest, '/AgencyChangeRequest')
ccwatsonip.add_resource(Auth, '/')
        
if __name__ == '__main__':
    app.run(debug=True)