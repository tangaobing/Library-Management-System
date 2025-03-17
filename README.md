# 图书管理系统

一个基于Flask+Vue3的图书管理系统，实现图书、分类、借阅和用户的管理功能。

## 技术架构

### 前端
- Vue 3 + Composition API
- Vue Router 4.x
- Pinia 状态管理
- Axios 1.3+
- Element Plus 2.3+
- 响应式布局

### 后端
- Python 3.9+
- Flask 2.2+
- Flask-SQLAlchemy 3.0+
- Flask-CORS 3.0+
- Flask-JWT-Extended 4.4+
- RESTful API 设计
- JWT 用户认证
- 请求参数校验
- 统一错误处理

### 数据库
- MySQL 8.0+
- 字符集 utf8mb4
- 索引优化
- 数据库连接池

## 功能模块

1. **图书管理**：CRUD + 模糊搜索 + 多条件筛选
2. **分类管理**：树形结构分类
3. **借阅管理**：借书/还书记录
4. **用户管理**：角色权限控制（基础版）

## 快速启动

### 后端

1. 创建虚拟环境（可选）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 配置数据库
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. 配置环境变量（可选）
```bash
# 创建.env文件
echo "SECRET_KEY=your_secret_key" > .env
echo "JWT_SECRET_KEY=your_jwt_secret_key" >> .env
echo "DATABASE_URI=mysql+pymysql://username:password@localhost/library_db?charset=utf8mb4" >> .env
```

5. 启动后端服务
```bash
python app.py
```

### 前端

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

## API文档

### 认证相关
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 图书相关
- `GET /api/books` - 获取图书列表
- `GET /api/books/{id}` - 获取图书详情
- `POST /api/books` - 创建图书
- `PUT /api/books/{id}` - 更新图书
- `DELETE /api/books/{id}` - 删除图书

### 分类相关
- `GET /api/categories` - 获取分类列表
- `GET /api/categories/{id}` - 获取分类详情
- `POST /api/categories` - 创建分类
- `PUT /api/categories/{id}` - 更新分类
- `DELETE /api/categories/{id}` - 删除分类

### 借阅相关
- `GET /api/borrows` - 获取借阅记录列表
- `GET /api/borrows/{id}` - 获取借阅记录详情
- `POST /api/borrows` - 借阅图书
- `POST /api/borrows/{id}/return` - 归还图书
- `POST /api/borrows/pay-fine` - 支付罚款
- `POST /api/borrows/check-overdue` - 检查逾期借阅

### 用户相关
- `GET /api/users` - 获取用户列表
- `GET /api/users/{id}` - 获取用户详情
- `POST /api/users` - 创建用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

## 项目结构

```
backend/
├── app.py              # 应用入口
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── models/             # 数据模型
│   ├── __init__.py
│   ├── book_model.py
│   ├── category_model.py
│   ├── user_model.py
│   └── borrow_model.py
├── controllers/        # 业务逻辑
│   ├── book_controller.py
│   ├── category_controller.py
│   ├── user_controller.py
│   └── borrow_controller.py
├── services/           # 服务层
│   ├── book_service.py
│   ├── category_service.py
│   ├── user_service.py
│   └── borrow_service.py
├── routes/             # 路由定义
│   ├── book_route.py
│   ├── category_route.py
│   ├── user_route.py
│   └── borrow_route.py
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

## 开发者

- 作者：全栈开发专家 