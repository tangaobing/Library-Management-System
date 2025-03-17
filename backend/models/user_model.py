from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    """
    用户模型
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='用户名')
    email = db.Column(db.String(100), unique=True, nullable=False, index=True, comment='邮箱')
    _password = db.Column('password', db.String(128), nullable=False, comment='密码')
    name = db.Column(db.String(50), comment='姓名')
    phone = db.Column(db.String(20), comment='电话')
    role = db.Column(
        db.Enum('admin', 'librarian', 'reader'), 
        default='reader',
        comment='角色: 管理员/图书管理员/读者'
    )
    status = db.Column(
        db.Enum('active', 'inactive', 'locked'), 
        default='active',
        comment='状态: 活跃/未激活/锁定'
    )
    avatar_url = db.Column(db.String(255), comment='头像URL')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系
    borrows = db.relationship('Borrow', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def password(self):
        """
        密码属性，不允许直接读取
        """
        raise AttributeError('密码不可读')
    
    @password.setter
    def password(self, password):
        """
        设置密码，自动进行哈希处理
        
        Args:
            password (str): 原始密码
        """
        self._password = generate_password_hash(password)
    
    def check_password(self, password):
        """
        验证密码
        
        Args:
            password (str): 待验证的密码
            
        Returns:
            bool: 密码是否正确
        """
        return check_password_hash(self._password, password)
    
    def update_last_login(self):
        """
        更新最后登录时间
        """
        self.last_login = datetime.now()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self, with_borrows=False):
        """
        将模型转换为字典
        
        Args:
            with_borrows (bool): 是否包含借阅信息
            
        Returns:
            dict: 用户信息字典
        """
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'status': self.status,
            'avatar': self.avatar_url,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if with_borrows:
            result['borrows'] = [borrow.to_dict() for borrow in self.borrows]
            
        return result 