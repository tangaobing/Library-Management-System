from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import ValidationError

from .response_util import ResponseUtil

error_bp = Blueprint('error_handler', __name__)

@error_bp.app_errorhandler(400)
def bad_request(e):
    """
    处理400错误
    
    Args:
        e: 异常对象
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.params_error(str(e))

@error_bp.app_errorhandler(401)
def unauthorized(e):
    """
    处理401错误
    
    Args:
        e: 异常对象
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.unauthorized(str(e))

@error_bp.app_errorhandler(403)
def forbidden(e):
    """
    处理403错误
    
    Args:
        e: 异常对象
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.forbidden(str(e))

@error_bp.app_errorhandler(404)
def not_found(e):
    """
    处理404错误
    
    Args:
        e: 异常对象
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.not_found(str(e))

@error_bp.app_errorhandler(ValidationError)
def validation_error(e):
    """
    处理参数验证错误
    
    Args:
        e: 验证错误异常
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.params_error(str(e))

@error_bp.app_errorhandler(SQLAlchemyError)
def db_error(e):
    """
    处理数据库错误
    
    Args:
        e: 数据库异常
        
    Returns:
        Response: 标准错误响应
    """
    return ResponseUtil.server_error(f"数据库错误: {str(e)}")

@error_bp.app_errorhandler(Exception)
def handle_exception(e):
    """
    处理所有未捕获的异常
    
    Args:
        e: 异常对象
        
    Returns:
        Response: 标准错误响应
    """
    # 如果是HTTP异常，使用其状态码
    if isinstance(e, HTTPException):
        return ResponseUtil.error(e.code, str(e))
    
    # 其他所有异常作为服务器错误处理
    return ResponseUtil.server_error(str(e))

def register_error_handlers(app):
    """
    注册所有错误处理器
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(error_bp) 