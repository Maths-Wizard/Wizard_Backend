from flask import Blueprint, request
from wizard.controllers.user import UserController, UserAuthentication
from wizard.utils.response import generate_response

user_bp = Blueprint('user', __name__, url_prefix='/user')
auth = UserAuthentication()

@user_bp.route('/', strict_slashes=False)
@auth.login_required
def user():
    user = UserController().findUser()
    user_obj = {
        'id': user.usr_id,
        'username': user.usr_name,
    }
    return generate_response(data=user_obj, status=200)
        
    
@user_bp.route('/change_password', methods=['POST'], strict_slashes=False)
@auth.login_required
def change_password():
    return UserController().changePassword()
