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

class IntentName(Resource):
    def get(self):
        return {'response': 'empty'}
        
class Auth(Resource):
    def get(self):
        print "Authentication made"
        return {'response': 'Authorized'}
        

# Pure rest
api.add_resource(IntentName, '/intent')
api.add_resource(Auth, '/')
        
if __name__ == '__main__':
    app.run(debug=True)