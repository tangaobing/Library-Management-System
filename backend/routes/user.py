from flask import Blueprint, request, jsonify, g
from models.user_model import User
from utils.auth_utils import login_required

user = Blueprint('user', __name__)

@user.route('/current', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    try:
        current_user = g.current_user
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'avatar': current_user.avatar,
                'phone': current_user.phone,
                'bio': current_user.bio
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@user.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """更新用户信息"""
    try:
        current_user = g.current_user
        if current_user.id != user_id:
            return jsonify({
                'code': 403,
                'message': '无权限修改其他用户信息'
            }), 403
            
        data = request.get_json()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在'
            }), 404
            
        # 更新用户信息
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        if 'bio' in data:
            user.bio = data['bio']
        if 'avatar' in data:
            user.avatar = data['avatar']
            
        user.save()
        
        return jsonify({
            'code': 0,
            'message': '更新成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar,
                'phone': user.phone,
                'bio': user.bio
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500 