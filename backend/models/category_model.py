from datetime import datetime
from . import db

class Category(db.Model):
    """
    图书分类模型
    实现树形结构的分类系统
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, index=True, comment='分类名称')
    code = db.Column(db.String(20), unique=True, comment='分类编码')
    description = db.Column(db.String(200), comment='分类描述')
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), comment='父分类ID')
    level = db.Column(db.Integer, default=1, comment='分类层级')
    sort_order = db.Column(db.Integer, default=0, comment='排序序号')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 自引用关系
    parent = db.relationship('Category', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """
        将模型转换为字典
        
        Returns:
            dict: 分类信息字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'parent_id': self.parent_id,
            'level': self.level,
            'sort_order': self.sort_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def to_tree_dict(self):
        """
        将模型转换为树形结构的字典
        
        Returns:
            dict: 包含子分类的分类信息字典
        """
        result = self.to_dict()
        children = self.children.order_by(Category.sort_order).all()
        if children:
            result['children'] = [child.to_tree_dict() for child in children]
        return result 