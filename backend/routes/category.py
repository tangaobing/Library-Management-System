from flask import Blueprint, request, jsonify
from controllers.category_controller import CategoryController
from utils.auth_utils import login_required

category = Blueprint('category', __name__)

@category.route('', methods=['GET', 'OPTIONS'])
@login_required
def get_categories():
    """获取所有分类"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
    return CategoryController.get_categories()

@category.route('/<int:category_id>', methods=['GET', 'OPTIONS'])
@login_required
def get_category(category_id):
    """获取分类详情"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
    return CategoryController.get_category(category_id)

@category.route('', methods=['POST', 'OPTIONS'])
@login_required
def create_category():
    """创建分类"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
    return CategoryController.create_category()

@category.route('/<int:category_id>', methods=['PUT', 'OPTIONS'])
@login_required
def update_category(category_id):
    """更新分类"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
    return CategoryController.update_category(category_id)

@category.route('/<int:category_id>', methods=['DELETE', 'OPTIONS'])
@login_required
def delete_category(category_id):
    """删除分类"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
    return CategoryController.delete_category(category_id) 