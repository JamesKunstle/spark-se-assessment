from json import dumps
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json()
        if post_data is None:
            responseObject = {
                'status': 'fail',
                'message': 'No JSON sent with request',
            }
            return make_response(jsonify(responseObject)), 401

        print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data['email']).first()
        if not user:
            try:
                user = User(
                    email=post_data['email'],
                    password=post_data['password']
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                """
                    James Kunstle: Previous problem with the auth_token not decoding 
                    because it's a string. String doesn't need to be decoded so we can just
                    return the value.
                """
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

"""
    Adding the endpoint /users/index,
    by James Kunstle for assessment assignment.
"""

class ListAPI(MethodView):
    """
    Users List Resource
    """

    def get(self):

        user_list = User.query.all()
        output_dict = {} 
        for user in user_list:
            output_dict[user.id] = {'admin': user.admin, 
                                          'email': user.email, 
                                          'registered_on': str(user.registered_on)}
        
        responseObject = {
            'users': output_dict 
        }

        return make_response(jsonify(responseObject)), 201


# define the API resources
list_view = ListAPI.as_view('list_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/users/index',
    view_func=list_view,
    methods=['GET']
)
