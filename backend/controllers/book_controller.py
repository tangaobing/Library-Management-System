from flask import request
from marshmallow import Schema, fields, validate, ValidationError

from services.book_service import BookService
from utils.response_util import ResponseUtil

class BookSchema(Schema):
    """图书数据验证模式"""
    isbn = fields.String(validate=validate.Length(max=20))
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    author = fields.String(required=True, validate=validate.Length(min=1, max=50))
    publisher = fields.String(validate=validate.Length(max=100))
    publish_date = fields.Date()
    price = fields.Decimal(places=2, allow_none=True)
    description = fields.String()
    cover_url = fields.String(validate=validate.Length(max=255))
    status = fields.String(validate=validate.OneOf(['available', 'borrowed', 'reserved', 'lost']))
    category_id = fields.Integer(allow_none=True)
    location = fields.String(validate=validate.Length(max=50))

class BookController:
    """
    图书控制器
    处理图书相关的请求
    """
    
    @staticmethod
    def get_books():
        """
        获取图书列表
        
        Returns:
            Response: 包含图书列表的响应
        """
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search')
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status')
        
        # 获取图书列表
        books, total = BookService.get_books(page, per_page, search, category_id, status)
        
        # 转换为字典
        book_list = [book.to_dict() for book in books]
        
        # 返回响应
        return ResponseUtil.success({
            'total': total,
            'page': page,
            'per_page': per_page,
            'books': book_list
        })
    
    @staticmethod
    def check_isbn_exists():
        """
        检查ISBN是否已存在
        
        Returns:
            Response: 包含检查结果的响应
        """
        # 获取查询参数
        isbn = request.args.get('isbn')
        
        if not isbn:
            return ResponseUtil.params_error("ISBN参数不能为空")
        
        # 检查ISBN是否存在
        exists = BookService.check_isbn_exists(isbn)
        
        # 返回响应
        return ResponseUtil.success({
            'exists': exists
        })
    
    @staticmethod
    def get_book(book_id):
        """
        获取图书详情
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            Response: 包含图书详情的响应
        """
        # 获取图书
        book = BookService.get_book_by_id(book_id)
        
        # 返回响应
        return ResponseUtil.success(book.to_dict())
    
    @staticmethod
    def create_book():
        """
        创建图书
        
        Returns:
            Response: 包含创建结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            book_data = BookSchema().load(data)
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        
        # 创建图书
        book = BookService.create_book(book_data)
        
        # 返回响应
        return ResponseUtil.success(book.to_dict(), "图书创建成功")
    
    @staticmethod
    def update_book(book_id):
        """
        更新图书
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            Response: 包含更新结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            book_data = BookSchema().load(data, partial=True)
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        
        # 更新图书
        book = BookService.update_book(book_id, book_data)
        
        # 返回响应
        return ResponseUtil.success(book.to_dict(), "图书更新成功")
    
    @staticmethod
    def delete_book(book_id):
        """
        删除图书
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            Response: 包含删除结果的响应
        """
        # 删除图书
        BookService.delete_book(book_id)
        
        # 返回响应
        return ResponseUtil.success(None, "图书删除成功") 