from flask import Blueprint
from controllers.category_controller import CategoryController
from utils.auth_utils import login_required

category = Blueprint('category', __name__)

@category.route('', methods=['GET'])
@login_required
def get_categories():
    """获取所有分类"""
    return CategoryController.get_categories()

@category.route('/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    """获取分类详情"""
    return CategoryController.get_category(category_id)

@category.route('', methods=['POST'])
@login_required
def create_category():
    """创建分类"""
    return CategoryController.create_category()

@category.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    """更新分类"""
    return CategoryController.update_category(category_id)

@category.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """删除分类"""
    return CategoryController.delete_category(category_id) 