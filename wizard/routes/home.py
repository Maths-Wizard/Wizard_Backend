from flask import Blueprint
from wizard.utils.response import generate_response
from wizard.utils.http_code import HTTP_200_OK

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    return generate_response(message='Welcome User!', status=HTTP_200_OK)
