from datetime import datetime, timedelta
from . import db

class Borrow(db.Model):
    """
    借阅记录模型
    """
    __tablename__ = 'borrows'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True, comment='图书ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True, comment='用户ID')
    borrow_date = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='借阅日期')
    due_date = db.Column(db.DateTime, nullable=False, comment='应还日期')
    return_date = db.Column(db.DateTime, comment='实际归还日期')
    status = db.Column(
        db.Enum('borrowing', 'returned', 'overdue', 'lost'), 
        default='borrowing',
        comment='状态: 借阅中/已归还/逾期/丢失'
    )
    fine_amount = db.Column(db.Numeric(10, 2), default=0, comment='罚款金额')
    fine_paid = db.Column(db.Boolean, default=False, comment='罚款是否已支付')
    remarks = db.Column(db.String(200), comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<Borrow {self.id}>'
    
    def to_dict(self):
        """
        将模型转换为字典
        
        Returns:
            dict: 借阅信息字典
        """
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d %H:%M:%S'),
            'due_date': self.due_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None,
            'status': self.status,
            'fine_amount': float(self.fine_amount) if self.fine_amount else 0,
            'fine_paid': self.fine_paid,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def calculate_due_date(borrow_date=None, days=14):
        """
        计算应还日期
        
        Args:
            borrow_date (datetime): 借阅日期，默认为当前时间
            days (int): 借阅天数，默认为14天
            
        Returns:
            datetime: 应还日期
        """
        if borrow_date is None:
            borrow_date = datetime.now()
        return borrow_date + timedelta(days=days)
    
    @staticmethod
    def calculate_fine(due_date, return_date=None, daily_rate=0.5):
        """
        计算罚款金额
        
        Args:
            due_date (datetime): 应还日期
            return_date (datetime): 实际归还日期，默认为当前时间
            daily_rate (float): 每天罚款金额，默认为0.5元
            
        Returns:
            float: 罚款金额
        """
        if return_date is None:
            return_date = datetime.now()
            
        if return_date <= due_date:
            return 0
            
        days_overdue = (return_date - due_date).days
        return days_overdue * daily_rate 