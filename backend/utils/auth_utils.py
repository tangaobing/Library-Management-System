from functools import wraps
from flask import request, jsonify, g
from models.user_model import User

def login_required(f):
    """
    登录验证装饰器
    使用简单的令牌认证替代JWT
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 从请求头中获取令牌
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    'code': 401,
                    'message': '未提供有效的认证令牌'
                }), 401
                
            token = auth_header.split(' ')[1]
            
            # 这里简化处理，实际应用中应该从数据库验证令牌
            # 假设我们有一个用户ID为1的管理员用户
            current_user = User.query.get(1)
            
            if not current_user:
                return jsonify({
                    'code': 401,
                    'message': '用户不存在'
                }), 401
                
            # 将用户信息存储在g对象中，以便视图函数使用
            g.current_user = current_user
            
        except Exception as e:
            return jsonify({
                'code': 401,
                'message': str(e)
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    获取当前登录用户
    
    Returns:
        User: 当前登录用户对象
    """
    return getattr(g, 'current_user', None) 