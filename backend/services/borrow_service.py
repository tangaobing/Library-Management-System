from datetime import datetime
from flask import abort

from models import db
from models.borrow_model import Borrow
from services.book_service import BookService
from services.user_service import UserService

class BorrowService:
    """
    借阅服务类
    处理图书借阅相关的业务逻辑
    """
    
    @staticmethod
    def get_borrows(page=1, per_page=10, user_id=None, book_id=None, status=None, book_title=None, user_name=None):
        """
        获取借阅记录列表，支持分页和筛选
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            user_id (int): 用户ID
            book_id (int): 图书ID
            status (str): 借阅状态
            book_title (str): 图书名称
            user_name (str): 用户名或姓名
            
        Returns:
            tuple: (借阅记录列表, 总数)
        """
        from models.book_model import Book
        from models.user_model import User
        
        query = Borrow.query.join(Book, Borrow.book_id == Book.id).join(User, Borrow.user_id == User.id)
        
        # 用户ID筛选                
        if user_id:
            query = query.filter(Borrow.user_id == user_id)
        
        # 图书ID筛选
        if book_id:
            query = query.filter(Borrow.book_id == book_id)
        
        # 状态筛选
        if status:
            query = query.filter(Borrow.status == status)
        
        # 图书名称筛选
        if book_title:
            query = query.filter(Book.title.like(f"%{book_title}%"))
        
        # 用户名或姓名筛选
        if user_name:
            query = query.filter((User.username.like(f"%{user_name}%")) | (User.name.like(f"%{user_name}%")))
        
        # 获取总数
        total = query.count()
        
        # 分页
        borrows = query.order_by(Borrow.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        return borrows.items, total
    
    @staticmethod
    def get_borrow_by_id(borrow_id):
        """
        根据ID获取借阅记录
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            Borrow: 借阅记录对象
            
        Raises:
            404: 如果借阅记录不存在
        """
        borrow = Borrow.query.get(borrow_id)
        if not borrow:
            abort(404, description=f"借阅记录ID {borrow_id} 不存在")
        return borrow
    
    @staticmethod
    def borrow_book(user_id, book_id, borrow_days=14, remarks=None):
        """
        借阅图书
        
        Args:
            user_id (int): 用户ID
            book_id (int): 图书ID
            borrow_days (int): 借阅天数
            remarks (str): 备注
            
        Returns:
            Borrow: 创建的借阅记录对象
            
        Raises:
            404: 如果用户或图书不存在
            400: 如果图书不可借
        """
        # 检查用户是否存在
        user = UserService.get_user_by_id(user_id)
        
        # 检查图书是否存在
        book = BookService.get_book_by_id(book_id)
        
        # 检查图书是否可借
        if book.status != 'available':
            abort(400, description="图书当前不可借阅")
        
        # 创建借阅记录
        borrow_date = datetime.now()
        due_date = Borrow.calculate_due_date(borrow_date, borrow_days)
        
        borrow = Borrow(
            book_id=book_id,
            user_id=user_id,
            borrow_date=borrow_date,
            due_date=due_date,
            status='borrowing',
            remarks=remarks
        )
        
        # 更新图书状态
        book.status = 'borrowed'
        
        db.session.add(borrow)
        db.session.commit()
        
        return borrow
    
    @staticmethod
    def return_book(borrow_id, is_lost=False):
        """
        归还图书
        
        Args:
            borrow_id (int): 借阅记录ID
            is_lost (bool): 是否丢失
            
        Returns:
            Borrow: 更新后的借阅记录对象
            
        Raises:
            404: 如果借阅记录不存在
            400: 如果借阅记录已归还
        """
        # 获取借阅记录
        borrow = BorrowService.get_borrow_by_id(borrow_id)
        
        # 检查是否已归还
        if borrow.status in ['returned', 'lost']:
            abort(400, description="图书已归还或已标记为丢失")
        
        # 获取图书
        book = BookService.get_book_by_id(borrow.book_id)
        
        # 更新借阅记录
        return_date = datetime.now()
        borrow.return_date = return_date
        
        if is_lost:
            borrow.status = 'lost'
            book.status = 'lost'
        else:
            borrow.status = 'returned'
            book.status = 'available'
            
            # 计算罚款
            if return_date > borrow.due_date:
                borrow.fine_amount = Borrow.calculate_fine(borrow.due_date, return_date)
                if borrow.fine_amount > 0:
                    borrow.status = 'overdue'
        
        db.session.commit()
        
        return borrow
    
    @staticmethod
    def pay_fine(borrow_id):
        """
        支付罚款
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            Borrow: 更新后的借阅记录对象
            
        Raises:
            404: 如果借阅记录不存在
            400: 如果没有罚款或已支付
        """
        # 获取借阅记录
        borrow = BorrowService.get_borrow_by_id(borrow_id)
        
        # 检查是否有罚款
        if float(borrow.fine_amount) <= 0:
            abort(400, description="没有需要支付的罚款")
        
        # 检查是否已支付
        if borrow.fine_paid:
            abort(400, description="罚款已支付")
        
        # 更新支付状态
        borrow.fine_paid = True
        
        # 如果状态是逾期，更新为已归还
        if borrow.status == 'overdue':
            borrow.status = 'returned'
        
        db.session.commit()
        
        return borrow
    
    @staticmethod
    def check_overdue_borrows():
        """
        检查逾期的借阅记录
        
        Returns:
            list: 逾期的借阅记录列表
        """
        now = datetime.now()
        
        # 查找所有借阅中且已逾期的记录
        overdue_borrows = Borrow.query.filter(
            Borrow.status == 'borrowing',
            Borrow.due_date < now
        ).all()
        
        # 更新状态为逾期
        for borrow in overdue_borrows:
            borrow.status = 'overdue'
            borrow.fine_amount = Borrow.calculate_fine(borrow.due_date, now)
        
        db.session.commit()
        
        return overdue_borrows
    
    @staticmethod
    def delete_borrow(borrow_id):
        """
        删除借阅记录
        
        Args:
            borrow_id (int): 借阅记录ID
            
        Returns:
            bool: 是否删除成功
            
        Raises:
            404: 如果借阅记录不存在
        """
        # 获取借阅记录
        borrow = BorrowService.get_borrow_by_id(borrow_id)
        
        # 如果借阅状态是借阅中，需要将图书状态恢复为可借阅
        if borrow.status == 'borrowing':
            book = BookService.get_book_by_id(borrow.book_id)
            book.status = 'available'
        
        # 删除借阅记录
        db.session.delete(borrow)
        db.session.commit()
        
        return True 