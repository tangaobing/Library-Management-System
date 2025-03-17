import jwt
from datetime import datetime, timedelta
from config import config
from flask import current_app

def create_token(user_id):
    """
    创建JWT token
    
    Args:
        user_id: 用户ID
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),  # 过期时间设为1天
        'iat': datetime.utcnow()  # 签发时间
    }
    
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """
    验证JWT token
    
    Args:
        token: JWT token
        
    Returns:
        dict: 解码后的payload
    """
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token已过期')
    except jwt.InvalidTokenError:
        raise Exception('无效的Token') 