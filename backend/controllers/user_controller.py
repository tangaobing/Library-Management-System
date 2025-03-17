from flask import request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity  # 注释掉JWT导入

from services.user_service import UserService
from utils.response_util import ResponseUtil

class UserSchema(Schema):
    """用户数据验证模式"""
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=6), load_only=True)
    name = fields.String(validate=validate.Length(max=50))
    phone = fields.String(validate=validate.Length(max=20))
    role = fields.String(validate=validate.OneOf(['admin', 'librarian', 'reader']))
    status = fields.String(validate=validate.OneOf(['active', 'inactive', 'locked']))
    avatar_url = fields.String(validate=validate.Length(max=255))

class LoginSchema(Schema):
    """登录数据验证模式"""
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserController:
    """
    用户控制器
    处理用户相关的请求
    """
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def get_users():
        """
        获取用户列表
        
        Returns:
            Response: 包含用户列表的响应
        """
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search')
        username = request.args.get('username')
        name = request.args.get('name')
        role = request.args.get('role')
        status = request.args.get('status')
        
        # 打印请求参数，便于调试
        print(f"查询参数: page={page}, per_page={per_page}, search={search}, username={username}, name={name}, role={role}, status={status}")
        
        try:
            # 从数据库获取用户列表
            users, total = UserService.get_users(
                page=page, 
                per_page=per_page, 
                search=search,
                username=username,
                name=name, 
                role=role, 
                status=status
            )
            
            # 转换为字典列表
            user_list = [user.to_dict() for user in users]
            
            # 返回响应
            return ResponseUtil.success({
                'total': total,
                'page': page,
                'per_page': per_page,
                'users': user_list
            })
        except Exception as e:
            print(f"获取用户列表出错: {str(e)}")
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def get_user(user_id):
        """
        获取用户详情
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Response: 包含用户详情的响应
        """
        try:
            # 从数据库获取用户
            user = UserService.get_user_by_id(user_id)
            
            # 返回响应
            return ResponseUtil.success(user.to_dict())
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def create_user():
        """
        创建用户
        
        Returns:
            Response: 包含创建结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            user_data = UserSchema().load(data)
            
            # 创建用户
            user = UserService.create_user(user_data)
            
            # 返回响应
            return ResponseUtil.success(user.to_dict(), "用户创建成功")
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def update_user(user_id):
        """
        更新用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Response: 包含更新结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            user_data = UserSchema().load(data, partial=True)
            
            # 更新用户
            user = UserService.update_user(user_id, user_data)
            
            # 返回响应
            return ResponseUtil.success(user.to_dict(), "用户更新成功")
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def delete_user(user_id):
        """
        删除用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Response: 包含删除结果的响应
        """
        try:
            # 删除用户
            UserService.delete_user(user_id)
            
            # 返回响应
            return ResponseUtil.success(None, "用户删除成功")
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    def login():
        """
        用户登录
        
        Returns:
            Response: 包含登录结果的响应
        """
        # 获取请求数据
        data = request.get_json()
        
        # 验证数据
        try:
            login_data = LoginSchema().load(data)
            
            # 使用用户服务进行认证
            user = UserService.authenticate(login_data['username'], login_data['password'])
            
            if user:
                # 用户认证成功
                # 创建访问令牌 - 注释掉JWT相关代码
                # access_token = create_access_token(identity=user.id)
                access_token = f'mock-token-for-{user.username}'  # 模拟token
                
                # 返回响应
                return ResponseUtil.success({
                    'access_token': access_token,
                    'user': user.to_dict()
                }, "登录成功")
            else:
                # 用户认证失败
                return ResponseUtil.unauthorized("用户名或密码错误")
            
        except ValidationError as e:
            return ResponseUtil.params_error(str(e))
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    # @jwt_required()  # 注释掉JWT装饰器
    def get_current_user():
        """
        获取当前登录用户信息
        
        Returns:
            Response: 包含当前用户信息的响应
        """
        try:
            # 从请求头中获取token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return ResponseUtil.unauthorized("未提供认证token")
            
            # 从token中提取用户名
            token = auth_header.split(' ')[-1]
            username = token.replace('mock-token-for-', '')
            
            # 获取用户信息
            user = UserService.get_user_by_username(username)
            if not user:
                return ResponseUtil.unauthorized("无效的token")
            
            # 返回响应
            return ResponseUtil.success(user.to_dict())
        except Exception as e:
            return ResponseUtil.server_error(str(e)) 