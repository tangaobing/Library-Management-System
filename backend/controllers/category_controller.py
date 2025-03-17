from flask import request
from marshmallow import Schema, fields, validate, ValidationError

from services.category_service import CategoryService
from utils.response_util import ResponseUtil

class CategorySchema(Schema):
    """分类数据验证模式"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    code = fields.String(validate=validate.Length(max=20))
    description = fields.String(validate=validate.Length(max=200))
    parent_id = fields.Integer(allow_none=True)
    sort_order = fields.Integer()

class CategoryController:
    """
    分类控制器
    处理图书分类相关的请求
    """
    
    @staticmethod
    def get_categories():
        """
        获取分类列表
        
        Returns:
            Response: 包含分类列表的响应
        """
        try:
            # 获取查询参数
            tree = request.args.get('tree', 'false').lower() == 'true'
            
            # 获取分类列表
            categories = CategoryService.get_categories(include_tree=tree)
            
            # 返回响应
            return ResponseUtil.success(categories)
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    def get_category(category_id):
        """
        获取分类详情
        
        Args:
            category_id (int): 分类ID
            
        Returns:
            Response: 包含分类详情的响应
        """
        try:
            # 获取分类
            category = CategoryService.get_category_by_id(category_id)
            
            # 返回响应
            return ResponseUtil.success(category.to_dict())
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    def create_category():
        """
        创建分类
        
        Returns:
            Response: 包含创建结果的响应
        """
        try:
            # 获取请求数据
            data = request.get_json()
            if not data:
                return ResponseUtil.params_error('请求数据不能为空')
            
            # 验证数据
            try:
                category_data = CategorySchema().load(data)
            except ValidationError as e:
                return ResponseUtil.params_error(str(e))
            
            # 创建分类
            category = CategoryService.create_category(category_data)
            
            # 返回响应
            return ResponseUtil.success(category.to_dict(), "分类创建成功")
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    def update_category(category_id):
        """
        更新分类
        
        Args:
            category_id (int): 分类ID
            
        Returns:
            Response: 包含更新结果的响应
        """
        try:
            # 获取请求数据
            data = request.get_json()
            if not data:
                return ResponseUtil.params_error('请求数据不能为空')
            
            # 验证数据
            try:
                category_data = CategorySchema().load(data, partial=True)
            except ValidationError as e:
                return ResponseUtil.params_error(str(e))
            
            # 更新分类
            category = CategoryService.update_category(category_id, category_data)
            
            # 返回响应
            return ResponseUtil.success(category.to_dict(), "分类更新成功")
        except Exception as e:
            return ResponseUtil.server_error(str(e))
    
    @staticmethod
    def delete_category(category_id):
        """
        删除分类
        
        Args:
            category_id (int): 分类ID
            
        Returns:
            Response: 包含删除结果的响应
        """
        try:
            # 删除分类
            CategoryService.delete_category(category_id)
            
            # 返回响应
            return ResponseUtil.success(None, "分类删除成功")
        except Exception as e:
            return ResponseUtil.server_error(str(e)) 