from datetime import datetime
from flask import abort

from models import db
from models.category_model import Category

class CategoryService:
    """
    分类服务类
    处理图书分类相关的业务逻辑
    """
    
    @staticmethod
    def get_categories(include_tree=False):
        """
        获取所有分类
        
        Args:
            include_tree (bool): 是否以树形结构返回
            
        Returns:
            list: 分类列表
        """
        if include_tree:
            # 只获取顶级分类，子分类通过关系获取
            root_categories = Category.query.filter(Category.parent_id.is_(None)).order_by(Category.sort_order).all()
            return [category.to_tree_dict() for category in root_categories]
        else:
            # 获取所有分类
            categories = Category.query.order_by(Category.level, Category.sort_order).all()
            return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        根据ID获取分类
        
        Args:
            category_id (int): 分类ID
            
        Returns:
            Category: 分类对象
            
        Raises:
            404: 如果分类不存在
        """
        category = Category.query.get(category_id)
        if not category:
            abort(404, description=f"分类ID {category_id} 不存在")
        return category
    
    @staticmethod
    def create_category(category_data):
        """
        创建新分类
        
        Args:
            category_data (dict): 分类数据
            
        Returns:
            Category: 创建的分类对象
        """
        # 如果有父分类，设置正确的level
        if category_data.get('parent_id'):
            parent = CategoryService.get_category_by_id(category_data['parent_id'])
            category_data['level'] = parent.level + 1
        else:
            category_data['level'] = 1
            
        category = Category(**category_data)
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def update_category(category_id, category_data):
        """
        更新分类信息
        
        Args:
            category_id (int): 分类ID
            category_data (dict): 更新的分类数据
            
        Returns:
            Category: 更新后的分类对象
            
        Raises:
            404: 如果分类不存在
        """
        category = CategoryService.get_category_by_id(category_id)
        
        # 如果更新了父分类，需要更新level
        if 'parent_id' in category_data and category_data['parent_id'] != category.parent_id:
            if category_data['parent_id']:
                parent = CategoryService.get_category_by_id(category_data['parent_id'])
                category_data['level'] = parent.level + 1
            else:
                category_data['level'] = 1
        
        # 更新字段
        for key, value in category_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        category.updated_at = datetime.now()
        db.session.commit()
        
        # 如果level发生变化，需要更新所有子分类的level
        if 'level' in category_data:
            CategoryService._update_children_level(category)
            
        return category
    
    @staticmethod
    def delete_category(category_id):
        """
        删除分类
        
        Args:
            category_id (int): 分类ID
            
        Returns:
            bool: 是否删除成功
            
        Raises:
            404: 如果分类不存在
            400: 如果分类下有子分类或图书
        """
        category = CategoryService.get_category_by_id(category_id)
        
        # 检查是否有子分类
        if category.children.count() > 0:
            abort(400, description="无法删除有子分类的分类")
        
        # 检查是否有图书
        if category.books.count() > 0:
            abort(400, description="无法删除有图书的分类")
        
        db.session.delete(category)
        db.session.commit()
        return True
    
    @staticmethod
    def _update_children_level(category):
        """
        递归更新子分类的level
        
        Args:
            category (Category): 父分类
        """
        for child in category.children:
            child.level = category.level + 1
            db.session.add(child)
            CategoryService._update_children_level(child)
        
        db.session.commit() 