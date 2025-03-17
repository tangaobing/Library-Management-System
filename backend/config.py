import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    # 应用配置
    SECRET_KEY = 'dev'
    DEBUG = False
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # JWT配置
    JWT_SECRET_KEY = 'jwt-secret-key'  # JWT密钥
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 访问令牌过期时间：1小时
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 刷新令牌过期时间：30天
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ERROR_MESSAGE_KEY = 'message'  # 错误消息的键名
    
    # CORS配置
    CORS_ORIGINS = [
        'http://localhost:5173',  # Vite开发服务器
        'http://localhost:4173',  # Vite预览服务器
        'http://localhost:3000',  # 其他可能的前端开发服务器
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
    # 生产环境应该使用更安全的密钥
    SECRET_KEY = 'production-secret-key'
    JWT_SECRET_KEY = 'production-jwt-secret-key'


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 