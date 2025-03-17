from flask import Flask, jsonify
from flask_cors import CORS
# 移除JWT相关导入
# from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

from config import config
from models import init_db
from routes.auth import auth
from routes.user import user
from routes.book import book
from routes.category import category
from routes.dashboard import dashboard

def create_app():
    """
    创建Flask应用
    
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config['development'])
    
    # 配置CORS，允许跨域请求 - 使用最简单的配置解决跨域问题
    # 允许所有来源的请求，支持凭证
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    
    # 移除JWT配置
    # jwt = JWTManager(app)
    
    # 移除JWT错误处理
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return jsonify({
    #         'code': 401,
    #         'message': '令牌已过期'
    #     }), 401
    #     
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return jsonify({
    #         'code': 401,
    #         'message': '无效的令牌'
    #     }), 401
    #     
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return jsonify({
    #         'code': 401,
    #         'message': '缺少令牌'
    #     }), 401
    
    # 初始化数据库
    init_db(app)
    
    # 注册所有的蓝图
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(user, url_prefix='/api/users')
    app.register_blueprint(book, url_prefix='/api/books')
    app.register_blueprint(category, url_prefix='/api/categories')
    app.register_blueprint(dashboard, url_prefix='/api/dashboard')
    
    return app

if __name__ == '__main__':
    app = create_app()
    # 启用调试模式，方便开发
    app.run(host='0.0.0.0', port=5000, debug=True) 