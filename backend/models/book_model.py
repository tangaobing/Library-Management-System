from datetime import datetime
from . import db

class Book(db.Model):
    """
    图书模型
    """
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, index=True, comment='ISBN编号')
    title = db.Column(db.String(100), nullable=False, index=True, comment='书名')
    author = db.Column(db.String(50), nullable=False, index=True, comment='作者')
    publisher = db.Column(db.String(100), comment='出版社')
    publish_date = db.Column(db.Date, comment='出版日期')
    price = db.Column(db.Numeric(10, 2), comment='价格')
    description = db.Column(db.Text, comment='图书描述')
    cover_url = db.Column(db.String(255), comment='封面图片URL')
    status = db.Column(
        db.Enum('available', 'borrowed', 'reserved', 'lost'), 
        default='available',
        comment='图书状态: 可借阅/已借出/已预约/丢失'
    )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), comment='分类ID')
    location = db.Column(db.String(50), comment='馆藏位置')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系
    category = db.relationship('Category', backref=db.backref('books', lazy='dynamic'))
    borrows = db.relationship('Borrow', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        """
        将模型转换为字典
        
        Returns:
            dict: 图书信息字典
        """
        return {
            'id': self.id,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publish_date': self.publish_date.strftime('%Y-%m-%d') if self.publish_date else None,
            'price': float(self.price) if self.price else None,
            'description': self.description,
            'cover_url': self.cover_url,
            'status': self.status,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'location': self.location,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 