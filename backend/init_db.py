from flask import Flask
from models import init_db, db
from models.user_model import User
from models.category_model import Category
from models.book_model import Book
from models.borrow_model import Borrow
from config import config
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(config['development'])

init_db(app)

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表
        db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        # 创建默认管理员用户
        admin = User(
            username='admin',
            email='admin@example.com',
            name='系统管理员',
            role='admin',
            status='active',
            avatar_url='/static/avatars/default.png'
        )
        admin.password = 'admin123'
        db.session.add(admin)
        
        # 创建默认图书分类
        categories = [
            Category(name='文学', description='包括小说、诗歌、散文等'),
            Category(name='科技', description='包括计算机、物理、化学等'),
            Category(name='历史', description='包括中国历史、世界历史等'),
            Category(name='艺术', description='包括音乐、绘画、雕塑等'),
            Category(name='哲学', description='包括中西方哲学等'),
            Category(name='经济', description='包括经济学、金融学等'),
            Category(name='教育', description='包括教育理论、教学方法等'),
            Category(name='其他', description='其他类别')
        ]
        db.session.add_all(categories)
        
        # 提交更改
        try:
            db.session.commit()
            print('数据库初始化成功！')
            print('默认管理员账号：admin')
            print('默认管理员密码：admin123')
        except Exception as e:
            db.session.rollback()
            print('数据库初始化失败：', str(e))

if __name__ == '__main__':
    init_database() 