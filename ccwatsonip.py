from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_basicauth import BasicAuth
import json

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'mwoods'
app.config['BASIC_AUTH_PASSWORD'] = 'hp92275a'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

api = Api(app)

beers = []

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
api.add_resource(Welcome, '/Welcome')
api.add_resource(Goodbye, '/Goodbye')
api.add_resource(Auth, '/')
        
if __name__ == '__main__':
    app.run(debug=True)