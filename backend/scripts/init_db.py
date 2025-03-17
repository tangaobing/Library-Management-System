import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from models import init_db, db
from models.user_model import User
from models.category_model import Category
from models.book_model import Book
from models.borrow_model import Borrow
from config import config

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config)
    init_db(app)
    return app

def init_test_data():
    """初始化测试数据"""
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        Borrow.query.delete()
        Book.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # 创建管理员用户
        admin = User()
        admin.username = 'admin'
        admin.password = 'admin123'
        admin.email = 'admin@example.com'
        admin.name = '管理员'
        admin.phone = '13800138000'
        admin.role = 'admin'
        admin.status = 'active'
        
        # 创建图书管理员用户
        librarian = User()
        librarian.username = 'librarian'
        librarian.password = 'librarian123'
        librarian.email = 'librarian@example.com'
        librarian.name = '图书管理员'
        librarian.phone = '13800138001'
        librarian.role = 'librarian'
        librarian.status = 'active'
        
        # 创建普通用户
        reader = User()
        reader.username = 'user'
        reader.password = 'user123'
        reader.email = 'user@example.com'
        reader.name = '普通用户'
        reader.phone = '13800138002'
        reader.role = 'reader'
        reader.status = 'active'
        
        # 添加用户到数据库
        db.session.add(admin)
        db.session.add(librarian)
        db.session.add(reader)
        
        # 创建图书分类
        literature = Category(name='文学', code='WX', description='文学类图书', level=1, sort_order=1)
        novel = Category(name='小说', code='WX-XS', description='小说类图书', level=2, sort_order=1)
        poetry = Category(name='诗歌', code='WX-SG', description='诗歌类图书', level=2, sort_order=2)
        
        computer = Category(name='计算机', code='JSJ', description='计算机类图书', level=1, sort_order=2)
        programming = Category(name='编程', code='JSJ-BC', description='编程类图书', level=2, sort_order=1)
        database = Category(name='数据库', code='JSJ-SJK', description='数据库类图书', level=2, sort_order=2)
        
        history = Category(name='历史', code='LS', description='历史类图书', level=1, sort_order=3)
        china_history = Category(name='中国历史', code='LS-ZG', description='中国历史类图书', level=2, sort_order=1)
        world_history = Category(name='世界历史', code='LS-SJ', description='世界历史类图书', level=2, sort_order=2)
        
        # 设置父子关系
        novel.parent = literature
        poetry.parent = literature
        programming.parent = computer
        database.parent = computer
        china_history.parent = history
        world_history.parent = history
        
        # 添加分类到数据库
        db.session.add_all([
            literature, novel, poetry,
            computer, programming, database,
            history, china_history, world_history
        ])
        
        # 提交以获取分类ID
        db.session.commit()
        
        # 创建图书
        books = [
            # 小说类
            Book(
                isbn='9787536692930',
                title='三体',
                author='刘慈欣',
                publisher='重庆出版社',
                publish_date=datetime(2008, 1, 1),
                price=23.00,
                description='科幻小说，描述人类文明与三体文明的恢宏故事。',
                status='available',
                category_id=novel.id,
                location='A区-1架-1列'
            ),
            Book(
                isbn='9787020002207',
                title='红楼梦',
                author='曹雪芹',
                publisher='人民文学出版社',
                publish_date=datetime(1996, 1, 1),
                price=59.70,
                description='中国古典四大名著之一。',
                status='borrowed',
                category_id=novel.id,
                location='A区-1架-2列'
            ),
            
            # 编程类
            Book(
                isbn='9787115546081',
                title='Python编程：从入门到实践',
                author='埃里克·马瑟斯',
                publisher='人民邮电出版社',
                publish_date=datetime(2020, 1, 1),
                price=89.00,
                description='Python入门经典教程。',
                status='available',
                category_id=programming.id,
                location='B区-1架-1列'
            ),
            Book(
                isbn='9787115537015',
                title='JavaScript高级程序设计',
                author='马特·弗里斯比',
                publisher='人民邮电出版社',
                publish_date=datetime(2020, 1, 1),
                price=119.00,
                description='JavaScript红宝书，程序员必读。',
                status='available',
                category_id=programming.id,
                location='B区-1架-2列'
            ),
            
            # 历史类
            Book(
                isbn='9787101003048',
                title='史记',
                author='司马迁',
                publisher='中华书局',
                publish_date=datetime(1959, 1, 1),
                price=125.00,
                description='中国史学家司马迁创作的一部纪传体通史。',
                status='available',
                category_id=china_history.id,
                location='C区-1架-1列'
            ),
            Book(
                isbn='9787100005043',
                title='世界文明史',
                author='威尔·杜兰特',
                publisher='商务印书馆',
                publish_date=datetime(2002, 1, 1),
                price=368.00,
                description='一部宏大的世界文明发展史。',
                status='reserved',
                category_id=world_history.id,
                location='C区-1架-2列'
            ),
        ]
        
        # 添加图书到数据库
        for book in books:
            db.session.add(book)
        
        # 提交以获取图书ID
        db.session.commit()
        
        # 创建借阅记录
        borrows = [
            # 已归还的借阅
            Borrow(
                book_id=books[0].id,  # 三体
                user_id=reader.id,
                borrow_date=datetime.now() - timedelta(days=30),
                due_date=datetime.now() - timedelta(days=16),
                return_date=datetime.now() - timedelta(days=18),
                status='returned',
                remarks='按时归还'
            ),
            # 当前借阅
            Borrow(
                book_id=books[1].id,  # 红楼梦
                user_id=reader.id,
                borrow_date=datetime.now() - timedelta(days=7),
                due_date=datetime.now() + timedelta(days=7),
                status='borrowing',
                remarks='首次借阅'
            ),
            # 逾期借阅
            Borrow(
                book_id=books[4].id,  # 史记
                user_id=librarian.id,
                borrow_date=datetime.now() - timedelta(days=30),
                due_date=datetime.now() - timedelta(days=16),
                status='overdue',
                fine_amount=7.00,
                remarks='已逾期'
            ),
        ]
        
        # 添加借阅记录到数据库
        for borrow in borrows:
            db.session.add(borrow)
        
        # 提交所有更改
        db.session.commit()
        
        print("测试数据初始化完成！")
        print("\n可用账号：")
        print("1. 管理员 - admin/admin123")
        print("2. 图书管理员 - librarian/librarian123")
        print("3. 普通用户 - user/user123")
        print("\n图书分类：")
        print("1. 文学（小说、诗歌）")
        print("2. 计算机（编程、数据库）")
        print("3. 历史（中国历史、世界历史）")
        print("\n示例图书：")
        print("1. 三体 - 刘慈欣")
        print("2. 红楼梦 - 曹雪芹")
        print("3. Python编程：从入门到实践")
        print("4. JavaScript高级程序设计")
        print("5. 史记 - 司马迁")
        print("6. 世界文明史")
        print("\n借阅记录：")
        print("1. 已归还 - 三体")
        print("2. 借阅中 - 红楼梦")
        print("3. 逾期 - 史记")

if __name__ == '__main__':
    init_test_data() 