from flask import request
from marshmallow import Schema, fields, validate, ValidationError
# from flask_jwt_extended import jwt_required, get_jwt_identity  # 注释掉JWT导入

from services.borrow_service import BorrowService
from services.user_service import UserService
from utils.response_util import ResponseUtil

class BorrowSchema(Schema):
    """借阅数据验证模式"""
    book_id = fields.Integer(required=True)
    user_id = fields.Integer()
    borrow_days = fields.Integer(validate=validate.Range(min=1, max=30))
    remarks = fields.String(validate=validate.Length(max=200))

class ReturnSchema(Schema):
    """归还数据验证模式"""
    is_lost = fields.Boolean(default=False)

class FineSchema(Schema):
    """罚款数据验证模式"""
    borrow_id = fields.Integer(required=True)

class BorrowController:
    """
    借阅控制器
    处理图书借阅相关的请求
    """
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def get_borrows():
        """
        获取借阅记录列表
        
        Returns:
            Response: 包含借阅记录列表的响应
        """
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        book_id = request.args.get('book_id', type=int)
        book_title = request.args.get('book_title')
        user_name = request.args.get('user_name')
        status = request.args.get('status')
        
        # 获取借阅记录列表
        borrows, total = BorrowService.get_borrows(
            page, 
            per_page, 
            user_id, 
            book_id, 
            status,
            book_title,
            user_name
        )
        
        # 转换为字典
        borrow_list = [borrow.to_dict() for borrow in borrows]
        
        # 返回响应
        return ResponseUtil.success({
            'total': total,
            'page': page,
            'per_page': per_page,
            'borrows': borrow_list
        })
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def get_borrow(borrow_id):
        """
        获取借阅记录详情
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            Response: 包含借阅记录详情的响应
        """
        # 获取借阅记录
        borrow = BorrowService.get_borrow_by_id(borrow_id)
        
        # 返回响应
        return ResponseUtil.success(borrow.to_dict())
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def borrow_book():
        """
        借阅图书
        
        Returns:
            Response: 包含借阅结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            borrow_data = BorrowSchema().load(data)
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        
        # 如果没有指定用户ID，尝试获取当前登录用户或使用默认用户
        # 检查 borrow_data 是否为字典且 'user_id' 不在其中
        if isinstance(borrow_data, dict) and 'user_id' not in borrow_data:
            # 尝试从请求头中获取token
            auth_header = request.headers.get('Authorization')
            if auth_header:
                # 从token中提取用户名
                token = auth_header.split(' ')[-1]
                username = token.replace('mock-token-for-', '')
                
                # 获取用户信息
                user = UserService.get_user_by_username(username)
                if user:
                    borrow_data['user_id'] = user.id
                else:
                    # 如果找不到用户，创建一个默认用户
                    default_user = UserService.get_or_create_default_user()
                    borrow_data['user_id'] = default_user.id
            else:
                # 如果没有认证头，创建一个默认用户
                default_user = UserService.get_or_create_default_user()
                borrow_data['user_id'] = default_user.id
        
        # 借阅图书
        borrow = BorrowService.borrow_book(
            borrow_data['user_id'],
            borrow_data['book_id'],
            borrow_data.get('borrow_days', 14),
            borrow_data.get('remarks')
        )
        
        # 返回响应
        return ResponseUtil.success(borrow.to_dict(), "图书借阅成功")
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def return_book(borrow_id):
        """
        归还图书
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            Response: 包含归还结果的响应
        """
        # 获取请求数据
        data = request.get_json() or {}
        
        # 验证数据
        try:
            return_data = ReturnSchema().load(data)
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        
        # 归还图书
        borrow = BorrowService.return_book(borrow_id, return_data.get('is_lost', False))
        
        # 返回响应+
        message = "图书归还成功"
        if borrow.status == 'lost':
            message = "图书已标记为丢失"
        elif borrow.status == 'overdue':
            message = f"图书已逾期归还，罚款 {borrow.fine_amount} 元"
        
        return ResponseUtil.success(borrow.to_dict(), message)
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def pay_fine():
        """
        支付罚款
        
        Returns:
            Response: 包含支付结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            fine_data = FineSchema().load(data)
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        
        # 支付罚款
        borrow = BorrowService.pay_fine(fine_data['borrow_id'])
        
        # 返回响应
        return ResponseUtil.success(borrow.to_dict(), "罚款支付成功")
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def check_overdue():
        """
        检查逾期借阅
        
        Returns:
            Response: 包含逾期借阅列表的响应
        """
        # 检查逾期借阅
        overdue_borrows = BorrowService.check_overdue_borrows()
        
        # 转换为字典
        overdue_list = [borrow.to_dict() for borrow in overdue_borrows]
        
        # 返回响应
        return ResponseUtil.success({
            'total': len(overdue_list),
            'overdue_borrows': overdue_list
        }, "逾期检查完成")
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def delete_borrow(borrow_id):
        """
        删除借阅记录
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            Response: 包含删除结果的响应
        """
        # 删除借阅记录
        BorrowService.delete_borrow(borrow_id)
        
        # 返回响应
        return ResponseUtil.success(None, "借阅记录删除成功") 