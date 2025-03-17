from flask import Blueprint, request, jsonify, current_app, session
from models.user_model import User
from models import db
from datetime import datetime, timedelta
import logging
import secrets
import jwt

auth = Blueprint('auth', __name__)

# JWT密钥
JWT_SECRET = 'your-secret-key'  # 在实际应用中应该使用环境变量

def generate_token(user_id):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # token有效期1天
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    """验证JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400,
                'message': '用户名和密码不能为空'
            }), 400
            
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
            
        # 生成token
        access_token = generate_token(user.id)
            
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'avatar_url': user.avatar_url,
                    'role': user.role,
                    'status': user.status
                }
            }
        })
    except Exception as e:
        current_app.logger.error(f"登录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@auth.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    创建新用户并返回访问令牌
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({
                'code': 400,
                'message': '用户名和密码不能为空'
            }), 400
            
        if User.query.filter_by(username=username).first():
            return jsonify({
                'code': 400,
                'message': '用户名已存在'
            }), 400
            
        if email and User.query.filter_by(email=email).first():
            return jsonify({
                'code': 400,
                'message': '邮箱已被使用'
            }), 400
            
        user = User(
            username=username,
            email=email
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        
        # 生成简单的访问令牌，不使用JWT
        access_token = secrets.token_hex(32)
        refresh_token = secrets.token_hex(32)
        
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'avatar_url': user.avatar_url,
                    'role': user.role,
                    'status': user.status
                }
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@auth.route('/refresh', methods=['POST'])
def refresh():
    """
    刷新访问令牌
    
    简化版的令牌刷新，不使用JWT
    """
    try:
        # 简单生成新的访问令牌
        new_access_token = secrets.token_hex(32)
        
        return jsonify({
            'code': 200,
            'message': '刷新成功',
            'data': {
                'access_token': new_access_token
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"刷新令牌失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@auth.route('/me', methods=['GET'])
def get_current_user():
    """获取当前登录用户信息"""
    try:
        # 从请求头中获取token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'code': 401,
                'message': '未提供有效的认证令牌'
            }), 401
            
        token = auth_header.split(' ')[1]
        
        # 验证token
        user_id = verify_token(token)
        if not user_id:
            return jsonify({
                'code': 401,
                'message': '认证令牌无效或已过期'
            }), 401
            
        # 获取用户信息
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在'
            }), 404
            
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar_url': user.avatar_url,
                'role': user.role,
                'status': user.status
            }
        })
    except Exception as e:
        current_app.logger.error(f"获取当前用户信息失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500 