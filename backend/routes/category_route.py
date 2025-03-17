from flask import Blueprint
from controllers.category_controller import CategoryController

# 创建蓝图
category_bp = Blueprint('category', __name__)

# 注册路由
category_bp.route('/', methods=['GET'])(CategoryController.get_categories)
category_bp.route('/<int:category_id>', methods=['GET'])(CategoryController.get_category)
category_bp.route('/', methods=['POST'])(CategoryController.create_category)
category_bp.route('/<int:category_id>', methods=['PUT'])(CategoryController.update_category)
category_bp.route('/<int:category_id>', methods=['DELETE'])(CategoryController.delete_category)

def register_category_routes(app):
    """
    注册分类相关路由
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(category_bp) 