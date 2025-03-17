from flask import Blueprint, request, jsonify, current_app, session
from models.user_model import User
from models import db
# 移除JWT相关导入
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     get_jwt_identity,
#     jwt_required,
#     get_jwt
# )
from datetime import timedelta
import logging
import secrets  # 用于生成随机token

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    使用简单的会话认证替代JWT
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '无效的请求数据'
            }), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400,
                'message': '用户名和密码不能为空'
            }), 400
            
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.status == 'locked':
                return jsonify({
                    'code': 403,
                    'message': '账号已被锁定'
                }), 403
                
            # 生成简单的访问令牌，不使用JWT
            access_token = secrets.token_hex(32)
            refresh_token = secrets.token_hex(32)
            
            # 更新最后登录时间
            try:
                user.update_last_login()
                # 可以在这里存储token到数据库，此处简化处理
                db.session.commit()
            except Exception as e:
                current_app.logger.error(f"更新登录时间失败: {str(e)}")
                db.session.rollback()
            
            # 返回成功响应
            return jsonify({
                'code': 200,
                'message': '登录成功',
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
        else:
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        current_app.logger.error(f"登录失败: {str(e)}")
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'服务器错误：{str(e)}'
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