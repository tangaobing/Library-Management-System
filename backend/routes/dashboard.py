from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from models.book_model import Book
from models.user_model import User
from models.borrow_model import Borrow
from models import db
from sqlalchemy import func

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    try:
        total_books = Book.query.count()
        total_users = User.query.count()
        total_borrows = Borrow.query.count()
        active_borrows = Borrow.query.filter_by(return_date=None).count()
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': {
                'totalBooks': total_books,
                'totalUsers': total_users,
                'totalBorrows': total_borrows,
                'activeBorrows': active_borrows
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'获取统计数据失败：{str(e)}'
        }), 500

@dashboard.route('/recent-borrows', methods=['GET'])
def get_recent_borrows():
    """获取最近借阅记录"""
    try:
        recent_borrows = db.session.query(
            Borrow, Book, User
        ).join(
            Book, Borrow.book_id == Book.id
        ).join(
            User, Borrow.user_id == User.id
        ).filter(
            Borrow.borrow_date >= (datetime.now() - timedelta(days=30))
        ).order_by(
            Borrow.borrow_date.desc()
        ).limit(10).all()
            
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': [{
                'id': record[0].id,
                'bookTitle': record[1].title,
                'userName': record[2].username,
                'borrowDate': record[0].borrow_date.strftime('%Y-%m-%d') if record[0].borrow_date else None,
                'returnDate': record[0].return_date.strftime('%Y-%m-%d') if record[0].return_date else None
            } for record in recent_borrows]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'获取最近借阅记录失败：{str(e)}'
        }), 500

@dashboard.route('/popular-books', methods=['GET'])
def get_popular_books():
    """获取热门图书"""
    try:
        # 使用子查询获取每本书的借阅次数
        popular_books = db.session.query(
            Book,
            func.count(Borrow.id).label('borrow_count')
        ).join(
            Borrow, Book.id == Borrow.book_id
        ).group_by(
            Book.id
        ).order_by(
            func.count(Borrow.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': [{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'borrowCount': borrow_count
            } for book, borrow_count in popular_books]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'获取热门图书失败：{str(e)}'
        }), 500 