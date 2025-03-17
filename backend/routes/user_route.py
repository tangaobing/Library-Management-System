from flask import Blueprint
from controllers.user_controller import UserController

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/users')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 用户路由
user_bp.route('/', methods=['GET'])(UserController.get_users)
user_bp.route('/<int:user_id>', methods=['GET'])(UserController.get_user)
user_bp.route('/', methods=['POST'])(UserController.create_user)
user_bp.route('/<int:user_id>', methods=['PUT'])(UserController.update_user)
user_bp.route('/<int:user_id>', methods=['DELETE'])(UserController.delete_user)

# 认证路由
auth_bp.route('/login', methods=['POST'])(UserController.login)
auth_bp.route('/me', methods=['GET'])(UserController.get_current_user)

def register_user_routes(app):
    """
    注册用户相关路由
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp) 