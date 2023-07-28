from flask import request
from wsgi import app
from wizard.utils.response import generate_response


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    return generate_response(message='Welcome User!', status=200)
