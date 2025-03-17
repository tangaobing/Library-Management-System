from flask import Blueprint
from controllers.book_controller import BookController

# 创建蓝图
book_bp = Blueprint('book', __name__, url_prefix='/api/books')

# 注册路由
book_bp.route('/', methods=['GET'])(BookController.get_books)
book_bp.route('/<int:book_id>', methods=['GET'])(BookController.get_book)
book_bp.route('/', methods=['POST'])(BookController.create_book)
book_bp.route('/<int:book_id>', methods=['PUT'])(BookController.update_book)
book_bp.route('/<int:book_id>', methods=['DELETE'])(BookController.delete_book)
book_bp.route('/check-isbn', methods=['GET'])(BookController.check_isbn_exists)

def register_book_routes(app):
    """
    注册图书相关路由
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(book_bp) 