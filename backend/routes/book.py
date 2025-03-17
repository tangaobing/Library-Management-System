from flask import Blueprint, request, jsonify
from models.book_model import Book
from utils.auth_utils import login_required

book = Blueprint('book', __name__)

@book.route('/', methods=['GET'])
def get_books():
    """获取图书列表"""
    try:
        books = Book.query.all()
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': [{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover': book.cover,
                'category_id': book.category_id,
                'category_name': book.category.name if book.category else None
            } for book in books]
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@book.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取图书详情"""
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'code': 404,
                'message': '图书不存在'
            }), 404
            
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover': book.cover,
                'category_id': book.category_id,
                'category_name': book.category.name if book.category else None
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500 