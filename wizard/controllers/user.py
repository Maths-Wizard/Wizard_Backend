from functools import wraps
import bcrypt
from flask import request, make_response
import jwt
from wizard.utils.token_generator import token_generator
from wizard.models.user import User
from wizard.utils.http_header import HEADER_AUTH_TOKEN
from wizard.utils.response_messages import LOGOUT_SUCCESS_MESSAGE, LOGIN_SUCCESS_MESSAGE, USER_CREATED_MESSAGE
from wizard.utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from wizard import db
from wizard.utils.response import generate_response


class AuthenticationError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = args[0]


class UserAuthentication:
    def login(self):
        try:
            user = UserController().findUser()
            if bcrypt.checkpw(request.json.get('password').encode('utf-8'), user.usr_password.encode('utf-8')):
                token = token_generator.encode_token(user)
                return self.setCookie(token)
            raise AuthenticationError(
                'Permission Denied, username or password is incorrect')
        except AuthenticationError as err:
            return make_response(generate_response(message=err.message, status=HTTP_401_UNAUTHORIZED))
        except Exception as err:
            print("falls through")
            print(err)
            return generate_response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def logout(self):
        response = make_response(generate_response(
            message=LOGOUT_SUCCESS_MESSAGE, status=HTTP_200_OK))
        response.delete_cookie(HEADER_AUTH_TOKEN)
        return response

    def setCookie(self, token):
        response = make_response(generate_response(
            message=LOGIN_SUCCESS_MESSAGE, status=HTTP_200_OK))
        response.set_cookie(HEADER_AUTH_TOKEN, token)
        return response

    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get(HEADER_AUTH_TOKEN)
            if not token:
                return generate_response(message='Not Logged in', status=401)
            try:
                token_generator.decode_token(token)
            except jwt.ExpiredSignatureError:
                return generate_response(message='Unauthorized', status=401)
            except jwt.InvalidTokenError:
                return generate_response(message='Invalid Token', status=401)
            return func(*args, **kwargs)
        return wrapper


class UserController:
    def createUser(self):
        newUser = {
            'usr_email': request.json.get('email'),
            'usr_name': request.json.get('username'),
            'usr_password': bcrypt.hashpw(request.json.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'usr_active_status': 'Y',
        }
        newUser = User(**newUser)
        db.session.add(newUser)
        db.session.commit()
        return generate_response(message=USER_CREATED_MESSAGE, status=HTTP_201_CREATED)

    def changePassword(self):
        try:
            user = self.findUser()
            if bcrypt.checkpw(request.json.get('password').encode('utf-8'), user.usr_password.encode('utf-8')):
                user.usr_password = bcrypt.hashpw(request.json.get(
                    'new_password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                db.session.add(user)
                db.session.commit()
                return generate_response(message="Password changed", status=HTTP_200_OK)
            else:
                return generate_response(message="Username or password incorrect", status=HTTP_401_UNAUTHORIZED)
        except AuthenticationError as err:
            return generate_response(message=err.message, status=HTTP_401_UNAUTHORIZED)

    def findUser(self):
        user = User.query.filter_by(
            usr_name=request.json.get('username')).first()
        if not user:
            print("user not found")
            raise AuthenticationError('User not found')
        return user
