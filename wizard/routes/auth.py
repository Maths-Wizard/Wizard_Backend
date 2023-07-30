from flask import Blueprint
from wizard.controllers.user import UserAuthentication, UserController

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    return UserAuthentication().login()


@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    return UserController().createUser()


@auth_bp.route('/logout', strict_slashes=False)
def logout():
    return UserAuthentication().logout()
