from datetime import datetime
from sqlalchemy import or_
from flask import abort

from models import db
from models.book_model import Book

class BookService:
    """
    图书服务类
    处理图书相关的业务逻辑
    """
    
    @staticmethod
    def get_books(page=1, per_page=10, search=None, category_id=None, status=None):
        """
        获取图书列表，支持分页、搜索和筛选
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            search (str): 搜索关键词
            category_id (int): 分类ID
            status (str): 图书状态
            
        Returns:
            tuple: (图书列表, 总数)
        """
        query = Book.query
        
        # 搜索条件
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Book.title.like(search_term),
                    Book.author.like(search_term),
                    Book.isbn.like(search_term),
                    Book.publisher.like(search_term)
                )
            )
        
        # 分类筛选
        if category_id:
            query = query.filter(Book.category_id == category_id)
        
        # 状态筛选
        if status:
            query = query.filter(Book.status == status)
        
        # 获取总数
        total = query.count()
        
        # 分页
        books = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        return books.items, total
    
    @staticmethod
    def get_book_by_id(book_id):
        """
        根据ID获取图书
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            Book: 图书对象
            
        Raises:
            404: 如果图书不存在
        """
        book = Book.query.get(book_id)
        if not book:
            abort(404, description=f"图书ID {book_id} 不存在")
        return book
    
    @staticmethod
    def create_book(book_data):
        """
        创建新图书
        
        Args:
            book_data (dict): 图书数据
            
        Returns:
            Book: 创建的图书对象
        """
        book = Book(**book_data)
        db.session.add(book)
        db.session.commit()
        return book
    
    @staticmethod
    def update_book(book_id, book_data):
        """
        更新图书信息
        
        Args:
            book_id (int): 图书ID
            book_data (dict): 更新的图书数据
            
        Returns:
            Book: 更新后的图书对象
            
        Raises:
            404: 如果图书不存在
        """
        book = BookService.get_book_by_id(book_id)
        
        # 更新字段
        for key, value in book_data.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        book.updated_at = datetime.now()
        db.session.commit()
        return book
    
    @staticmethod
    def delete_book(book_id):
        """
        删除图书
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            bool: 是否删除成功
            
        Raises:
            404: 如果图书不存在
        """
        book = BookService.get_book_by_id(book_id)
        db.session.delete(book)
        db.session.commit()
        return True
    
    @staticmethod
    def check_isbn_exists(isbn):
        """
        检查ISBN是否已存在
        
        Args:
            isbn (str): ISBN编号
            
        Returns:
            bool: ISBN是否已存在
        """
        return Book.query.filter_by(isbn=isbn).first() is not None
    
    @staticmethod
    def check_book_availability(book_id):
        """
        检查图书是否可借
        
        Args:
            book_id (int): 图书ID
            
        Returns:
            bool: 图书是否可借
            
        Raises:
            404: 如果图书不存在
        """
        book = BookService.get_book_by_id(book_id)
        return book.status == 'available'
    
    @staticmethod
    def update_book_status(book_id, status):
        """
        更新图书状态
        
        Args:
            book_id (int): 图书ID
            status (str): 新状态
            
        Returns:
            Book: 更新后的图书对象
            
        Raises:
            404: 如果图书不存在
        """
        book = BookService.get_book_by_id(book_id)
        book.status = status
        book.updated_at = datetime.now()
        db.session.commit()
        return book 