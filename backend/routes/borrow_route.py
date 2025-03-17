from flask import Blueprint
from controllers.borrow_controller import BorrowController

# 创建蓝图
borrow_bp = Blueprint('borrow', __name__, url_prefix='/api/borrows')

# 注册路由
borrow_bp.route('/', methods=['GET'])(BorrowController.get_borrows)
borrow_bp.route('/<int:borrow_id>', methods=['GET'])(BorrowController.get_borrow)
borrow_bp.route('/', methods=['POST'])(BorrowController.borrow_book)
borrow_bp.route('/<int:borrow_id>/return', methods=['POST'])(BorrowController.return_book)
borrow_bp.route('/pay-fine', methods=['POST'])(BorrowController.pay_fine)
borrow_bp.route('/check-overdue', methods=['POST'])(BorrowController.check_overdue)
borrow_bp.route('/<int:borrow_id>', methods=['DELETE'])(BorrowController.delete_borrow)

def register_borrow_routes(app):
    """
    注册借阅相关路由
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(borrow_bp) 