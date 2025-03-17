from datetime import datetime
from flask import abort
from sqlalchemy import or_

from models import db
from models.user_model import User
from models.borrow_model import Borrow

class UserService:
    """
    用户服务类
    处理用户相关的业务逻辑
    """
    
    @staticmethod
    def get_users(page=1, per_page=10, search=None, username=None, name=None, role=None, status=None):
        """
        获取用户列表，支持分页、搜索和筛选
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            search (str): 搜索关键词
            username (str): 用户名搜索
            name (str): 姓名搜索
            role (str): 用户角色
            status (str): 用户状态
            
        Returns:
            tuple: (用户列表, 总数)
        """
        query = User.query
        
        # 搜索条件
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.like(search_term),
                    User.email.like(search_term),
                    User.name.like(search_term),
                    User.phone.like(search_term)
                )
            )
        
        # 用户名搜索
        if username:
            query = query.filter(User.username.like(f"%{username}%"))
        
        # 姓名搜索
        if name:
            query = query.filter(User.name.like(f"%{name}%"))
        
        # 角色筛选
        if role:
            query = query.filter(User.role == role)
        
        # 状态筛选
        if status:
            query = query.filter(User.status == status)
        
        # 获取总数
        total = query.count()
        
        # 分页
        users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        return users.items, total
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        根据ID获取用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            User: 用户对象
            
        Raises:
            404: 如果用户不存在
        """
        user = User.query.get(user_id)
        if not user:
            abort(404, description=f"用户ID {user_id} 不存在")
        return user
    
    @staticmethod
    def get_user_by_username(username):
        """
        根据用户名获取用户
        
        Args:
            username (str): 用户名
            
        Returns:
            User: 用户对象，如果不存在则返回None
        """
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """
        根据邮箱获取用户
        
        Args:
            email (str): 邮箱
            
        Returns:
            User: 用户对象，如果不存在则返回None
        """
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(user_data):
        """
        创建新用户
        
        Args:
            user_data (dict): 用户数据
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            400: 如果用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        if UserService.get_user_by_username(user_data.get('username')):
            abort(400, description="用户名已存在")
        
        # 检查邮箱是否已存在
        if UserService.get_user_by_email(user_data.get('email')):
            abort(400, description="邮箱已存在")
        
        # 创建用户
        user = User()
        
        # 设置密码
        if 'password' in user_data:
            user.password = user_data.pop('password')
        
        # 设置其他字段
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, user_data):
        """
        更新用户信息
        
        Args:
            user_id (int): 用户ID
            user_data (dict): 更新的用户数据
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            404: 如果用户不存在
            400: 如果用户名或邮箱已被其他用户使用
        """
        user = UserService.get_user_by_id(user_id)
        
        # 检查用户名是否已被其他用户使用
        if 'username' in user_data and user_data['username'] != user.username:
            existing_user = UserService.get_user_by_username(user_data['username'])
            if existing_user and existing_user.id != user_id:
                abort(400, description="用户名已存在")
        
        # 检查邮箱是否已被其他用户使用
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = UserService.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                abort(400, description="邮箱已存在")
        
        # 更新密码
        if 'password' in user_data:
            user.password = user_data.pop('password')
        
        # 更新其他字段
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """
        删除用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            bool: 是否删除成功
            
        Raises:
            404: 如果用户不存在
            400: 如果用户有未归还的借阅记录
        """
        user = UserService.get_user_by_id(user_id)
        
        # 检查用户是否有未归还的借阅记录
        active_borrows = Borrow.query.filter(
            Borrow.user_id == user_id,
            Borrow.status.in_(['borrowing', 'overdue'])
        ).count()
        
        if active_borrows > 0:
            abort(400, description=f"无法删除用户，该用户有{active_borrows}条未归还的借阅记录")
        
        # 获取用户的所有借阅记录
        borrows = Borrow.query.filter(Borrow.user_id == user_id).all()
        
        # 删除用户的所有借阅记录
        for borrow in borrows:
            db.session.delete(borrow)
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def authenticate(username, password):
        """
        用户认证
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            User: 认证成功的用户对象，如果认证失败则返回None
        """
        user = UserService.get_user_by_username(username)
        
        if user and user.verify_password(password):
            # 更新最后登录时间
            user.last_login = datetime.now()
            db.session.commit()
            return user
        
        return None
    
    @staticmethod
    def update_user_status(user_id, status):
        """
        更新用户状态
        
        Args:
            user_id (int): 用户ID
            status (str): 新状态
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            404: 如果用户不存在
        """
        user = UserService.get_user_by_id(user_id)
        user.status = status
        user.updated_at = datetime.now()
        db.session.commit()
        return user
    
    @staticmethod
    def get_or_create_default_user():
        """
        获取或创建默认用户
        
        Returns:
            User: 默认用户对象
        """
        # 尝试获取默认用户
        default_user = User.query.filter_by(username='default_user').first()
        
        # 如果不存在，创建一个
        if not default_user:
            default_user = User(
                username='default_user',
                name='默认用户',
                email='default@example.com',
                role='user',
                status='active'
            )
            default_user.password = 'default123'  # 设置默认密码
            db.session.add(default_user)
            db.session.commit()
        
        return default_user 