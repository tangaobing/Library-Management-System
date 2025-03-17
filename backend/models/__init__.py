from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建SQLAlchemy实例
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """
    初始化数据库
    
    Args:
        app: Flask应用实例
    """
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 导入所有模型以确保它们被注册
    from .book_model import Book
    from .category_model import Category
    from .user_model import User
    from .borrow_model import Borrow
    
    # 创建所有表
    with app.app_context():
        db.create_all() 