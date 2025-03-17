from flask import Blueprint, request, jsonify
from models.book_model import Book
from models import db
from utils.auth_utils import login_required

book = Blueprint('book', __name__)

@book.route('', methods=['GET', 'OPTIONS'])
@login_required
def get_books():
    """获取图书列表"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
        
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status', '')
        
        # 构建查询
        query = Book.query
        
        # 添加搜索条件
        if search:
            query = query.filter(Book.title.ilike(f'%{search}%'))
            
        # 添加分类过滤
        if category_id:
            query = query.filter_by(category_id=category_id)
            
        # 添加状态过滤
        if status:
            query = query.filter_by(status=status)
            
        # 执行分页查询
        pagination = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'items': [{
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'cover': book.cover,
                    'category_id': book.category_id,
                    'category_name': book.category.name if book.category else None,
                    'status': book.status,
                    'description': book.description,
                    'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S') if book.created_at else None,
                    'updated_at': book.updated_at.strftime('%Y-%m-%d %H:%M:%S') if book.updated_at else None
                } for book in pagination.items],
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@book.route('/<int:book_id>', methods=['GET', 'OPTIONS'])
@login_required
def get_book(book_id):
    """获取图书详情"""
    if request.method == 'OPTIONS':
        return jsonify({'code': 200, 'message': 'OK'})
        
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({
                'code': 404,
                'message': '图书不存在'
            }), 404
            
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'cover': book.cover,
                'category_id': book.category_id,
                'category_name': book.category.name if book.category else None,
                'status': book.status,
                'description': book.description,
                'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S') if book.created_at else None,
                'updated_at': book.updated_at.strftime('%Y-%m-%d %H:%M:%S') if book.updated_at else None
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500 