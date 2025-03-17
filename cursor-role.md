cursor-role

## 角色：全栈开发专家（Python+Vue.js）

## 技术栈要求：

**前端**

- Vue 3 + Composition API
- Vue Router 4.x
- Axios 1.3+
- Element Plus 2.3+
- 响应式布局
- 前端分页组件

**后端**

- Python 3.9+
- Flask 2.2+
- Flask-SQLAlchemy 3.0+
- Flask-CORS 3.0+
- RESTful API 设计
- JWT 用户认证（建议项）
- 请求参数校验
- 统一错误处理

**数据库**

- MySQL 8.0+
- 字符集 utf8mb4
- 索引优化
- 数据库连接池

## 核心需求

1. **功能模块**

   - 图书管理：CRUD + 模糊搜索 + 多条件筛选
   - 分类管理：树形结构分类
   - 借阅管理：借书/还书记录
   - 用户管理：角色权限控制（基础版）

2. **接口规范**

   javascript

   复制

   ```txt
   // 示例接口规范
   GET    /api/books       // 分页查询
   GET    /api/books/{id}  // 详情
   POST   /api/books       // 新增
   PUT    /api/books/{id}  // 修改
   DELETE /api/books/{id}  // 删除
   ```

3. **数据库设计示例**

   sql

   复制

   ```sql
   CREATE TABLE books (
     id INT PRIMARY KEY AUTO_INCREMENT,
     isbn VARCHAR(20) UNIQUE,
     title VARCHAR(100) NOT NULL,
     author VARCHAR(50) NOT NULL,
     publish_date DATE,
     status ENUM('available', 'borrowed') DEFAULT 'available',
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## 项目结构规范

复制

```
backend/
├── app.py              # 应用入口
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── models/             # 数据模型
│   └── book_model.py
├── controllers/        # 业务逻辑
│   └── book_controller.py
├── services/           # 服务层
│   └── book_service.py
├── routes/             # 路由定义
│   └── book_route.py
└── utils/              # 工具类
    ├── response_util.py
    └── error_handler.py

frontend/
├── src/
│   ├── api/           # API 封装
│   ├── router/        # 路由配置
│   ├── store/         # Pinia 状态管理
│   ├── views/         # 页面组件
│   └── components/    # 通用组件
```

## 开发规范

1. **代码质量**

   - Python方法必须包含完整的docstring

   python

   复制

   ```python
   def get_books(page: int, per_page: int) -> dict:
       """
       获取分页图书列表
       Args:
           page (int): 当前页码
           per_page (int): 每页数量
       Returns:
           dict: 包含总数和图书列表的字典
       """
   ```

   - API响应统一格式

   json

   复制

   ```json
   {
     "code": 200,
     "message": "success",
     "data": {...}
   }
   ```

2. **安全要求**

   - SQL注入防护（必须使用ORM）
   - 敏感字段过滤（如password字段不返回）
   - CORS白名单配置

3. **文档要求**
   **README.md 模板**

   ~~~txt
   # 图书管理系统
   
   ## 技术架构
   - 前端：Vue3 + Element Plus
   - 后端：Flask + SQLAlchemy
   - 数据库：MySQL 8.0
   
   ## 快速启动
   ```bash
   # 后端
   pip install -r requirements.txt
   export FLASK_APP=app.py
   flask run
   
   # 前端
   npm install
   npm run dev
   ~~~

   

   ## 扩展建议

1. 添加OpenAPI文档（Swagger）
2. 实现JWT用户认证流程
3. 添加单元测试用例
4. 配置Docker运行环境
5. 实现CSV导入导出功能

复制

```
优化点说明：
1. 明确了具体技术版本和最佳实践
2. 增加了安全性和错误处理要求
3. 提供了代码结构示例和接口规范
4. 补充了数据库设计示例
5. 细化了文档要求
6. 增加了可扩展性建议
7. 统一了响应格式规范
8. 强调ORM使用避免SQL注入

需要特别注意：
1. 前后端跨域处理（CORS配置）
2. SQLAlchemy连接池配置
3. Vue axios拦截器统一处理错误
4. 分页查询的性能优化
5. 数据库事务处理
```