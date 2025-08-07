# RBAC权限管理系统

基于FastAPI实现的RBAC（基于角色的访问控制）权限管理系统，提供完整的用户、角色、权限管理功能。

## 功能特性

- 🔐 **JWT认证**: 基于JWT的用户认证系统
- 👥 **用户管理**: 用户的增删改查操作
- 🎭 **角色管理**: 角色的创建、分配和管理
- 🔑 **权限管理**: 细粒度的权限控制
- 🛡️ **权限验证**: 基于注解的权限验证装饰器
- 📚 **API文档**: 自动生成的Swagger文档
- 🗄️ **数据库支持**: 支持SQLite和PostgreSQL

## 项目结构

```
rbac/
├── models.py              # 数据库模型
├── schemas.py             # Pydantic数据模式
├── database.py            # 数据库连接配置
├── auth.py                # 认证和权限验证
├── crud.py                # 数据库操作函数
├── main.py                # 主应用文件
├── init_data.py           # 初始化数据脚本
├── run.py                 # 启动脚本
├── requirements.txt       # 依赖包列表
├── routers/               # 路由模块
│   ├── __init__.py
│   ├── auth.py            # 认证相关路由
│   ├── users.py           # 用户管理路由
│   ├── roles.py           # 角色管理路由
│   └── permissions.py     # 权限管理路由
└── README.md              # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
cd rbac
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///./rbac.db

# JWT配置
SECRET_KEY=your-secret-key-here

# 可选：使用PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost/rbac_db
```

### 3. 运行应用

```bash
# 方式1：直接运行
python -m rbac.run

# 方式2：使用uvicorn
uvicorn rbac.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问应用

- 应用地址: http://localhost:8000
- API文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc

## 默认账户

系统初始化后会创建以下默认账户：

- **用户名**: admin
- **密码**: admin123
- **角色**: 超级管理员

⚠️ **注意**: 请及时修改默认密码！

## API接口

### 认证接口

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/register` - 用户注册
- `GET /api/v1/auth/me` - 获取当前用户信息
- `GET /api/v1/auth/me/permissions` - 获取当前用户权限
- `POST /api/v1/auth/check-permission` - 检查权限

### 用户管理

- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建用户
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户
- `POST /api/v1/users/{user_id}/roles` - 为用户分配角色
- `GET /api/v1/users/{user_id}/roles` - 获取用户角色

### 角色管理

- `GET /api/v1/roles/` - 获取角色列表
- `POST /api/v1/roles/` - 创建角色
- `GET /api/v1/roles/{role_id}` - 获取角色详情
- `PUT /api/v1/roles/{role_id}` - 更新角色
- `DELETE /api/v1/roles/{role_id}` - 删除角色
- `POST /api/v1/roles/{role_id}/permissions` - 为角色分配权限
- `GET /api/v1/roles/{role_id}/permissions` - 获取角色权限

### 权限管理

- `GET /api/v1/permissions/` - 获取权限列表
- `POST /api/v1/permissions/` - 创建权限
- `GET /api/v1/permissions/{permission_id}` - 获取权限详情
- `PUT /api/v1/permissions/{permission_id}` - 更新权限
- `DELETE /api/v1/permissions/{permission_id}` - 删除权限
- `GET /api/v1/permissions/resource/{resource}` - 根据资源获取权限

## 权限验证

### 使用权限验证装饰器

```python
from fastapi import Depends
from rbac.auth import require_permission, require_role

@app.get("/protected-resource")
def protected_endpoint(
    current_user = Depends(require_permission("resource", "action"))
):
    return {"message": "访问成功"}

@app.get("/admin-only")
def admin_endpoint(
    current_user = Depends(require_role("管理员"))
):
    return {"message": "管理员专用"}
```

### 权限格式

权限格式为：`资源:操作`

- **资源**: 如 `users`, `roles`, `permissions`, `system`
- **操作**: 如 `create`, `read`, `update`, `delete`, `manage`

### 预定义权限

系统包含以下预定义权限：

- `users:read` - 查看用户
- `users:create` - 创建用户
- `users:update` - 更新用户
- `users:delete` - 删除用户
- `roles:read` - 查看角色
- `roles:create` - 创建角色
- `roles:update` - 更新角色
- `roles:delete` - 删除角色
- `permissions:read` - 查看权限
- `permissions:create` - 创建权限
- `permissions:update` - 更新权限
- `permissions:delete` - 删除权限
- `system:read` - 查看系统信息
- `system:manage` - 管理系统设置

## 数据库模型

### 用户表 (users)
- id: 主键
- username: 用户名
- email: 邮箱
- hashed_password: 密码哈希
- is_active: 是否激活
- created_at: 创建时间
- updated_at: 更新时间

### 角色表 (roles)
- id: 主键
- name: 角色名称
- description: 角色描述
- is_active: 是否激活
- created_at: 创建时间
- updated_at: 更新时间

### 权限表 (permissions)
- id: 主键
- name: 权限名称
- resource: 资源名称
- action: 操作类型
- description: 权限描述
- is_active: 是否激活
- created_at: 创建时间
- updated_at: 更新时间

### 关联表
- user_role: 用户-角色关联表
- role_permission: 角色-权限关联表

## 开发指南

### 添加新的权限验证

1. 在 `auth.py` 中定义权限验证函数
2. 在路由中使用 `Depends(require_permission("resource", "action"))`
3. 确保数据库中已创建对应的权限记录

### 自定义权限检查

```python
from rbac.auth import has_permission

def custom_permission_check(user, resource, action, db):
    return has_permission(user, resource, action, db)
```

### 扩展数据模型

1. 在 `models.py` 中添加新的模型类
2. 在 `schemas.py` 中添加对应的Pydantic模式
3. 在 `crud.py` 中添加CRUD操作函数
4. 创建对应的路由文件

## 部署

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "rbac.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

1. 使用PostgreSQL数据库
2. 设置强密码的SECRET_KEY
3. 配置HTTPS
4. 设置适当的CORS策略
5. 启用日志记录

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 