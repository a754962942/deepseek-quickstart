"""
RBAC权限管理系统使用示例
展示如何在FastAPI中使用权限验证装饰器
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

# 导入RBAC模块
from .database import get_db
from . import auth, schemas

# 创建示例应用
app = FastAPI(title="RBAC使用示例")

# 示例1: 使用权限验证装饰器
@app.get("/api/users/profile")
def get_user_profile(
    current_user: schemas.User = Depends(auth.require_permission("users", "read"))
):
    """获取用户资料 - 需要users:read权限"""
    return {
        "message": "用户资料",
        "user_id": current_user.id,
        "username": current_user.username
    }

@app.post("/api/users")
def create_user(
    user_data: schemas.UserCreate,
    current_user: schemas.User = Depends(auth.require_permission("users", "create")),
    db: Session = Depends(get_db)
):
    """创建用户 - 需要users:create权限"""
    # 这里可以添加创建用户的逻辑
    return {
        "message": "用户创建成功",
        "username": user_data.username,
        "created_by": current_user.username
    }

@app.put("/api/users/{user_id}")
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: schemas.User = Depends(auth.require_permission("users", "update")),
    db: Session = Depends(get_db)
):
    """更新用户 - 需要users:update权限"""
    return {
        "message": "用户更新成功",
        "user_id": user_id,
        "updated_by": current_user.username
    }

@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: schemas.User = Depends(auth.require_permission("users", "delete")),
    db: Session = Depends(get_db)
):
    """删除用户 - 需要users:delete权限"""
    return {
        "message": "用户删除成功",
        "user_id": user_id,
        "deleted_by": current_user.username
    }

# 示例2: 使用角色验证装饰器
@app.get("/api/admin/dashboard")
def admin_dashboard(
    current_user: schemas.User = Depends(auth.require_role("管理员"))
):
    """管理员仪表板 - 需要管理员角色"""
    return {
        "message": "管理员仪表板",
        "user": current_user.username,
        "role": "管理员"
    }

@app.get("/api/super-admin/system")
def super_admin_system(
    current_user: schemas.User = Depends(auth.require_role("超级管理员"))
):
    """超级管理员系统设置 - 需要超级管理员角色"""
    return {
        "message": "超级管理员系统设置",
        "user": current_user.username,
        "role": "超级管理员"
    }

# 示例3: 自定义权限检查
@app.get("/api/custom/resource")
def custom_resource(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """自定义权限检查示例"""
    # 检查用户是否有特定权限
    if not auth.has_permission(current_user, "custom", "read", db):
        raise HTTPException(status_code=403, detail="权限不足")
    
    return {
        "message": "自定义资源访问成功",
        "user": current_user.username
    }

# 示例4: 多权限检查
@app.get("/api/multi-permission/resource")
def multi_permission_resource(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """多权限检查示例"""
    # 检查多个权限
    required_permissions = [
        ("users", "read"),
        ("roles", "read")
    ]
    
    for resource, action in required_permissions:
        if not auth.has_permission(current_user, resource, action, db):
            raise HTTPException(
                status_code=403, 
                detail=f"权限不足: 需要 {resource}:{action} 权限"
            )
    
    return {
        "message": "多权限资源访问成功",
        "user": current_user.username,
        "permissions": auth.get_user_permissions(current_user, db)
    }

# 示例5: 条件权限检查
@app.get("/api/conditional/resource/{resource_id}")
def conditional_resource(
    resource_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """条件权限检查示例"""
    # 根据资源ID决定需要的权限
    if resource_id <= 100:
        required_permission = ("public", "read")
    else:
        required_permission = ("private", "read")
    
    if not auth.has_permission(current_user, required_permission[0], required_permission[1], db):
        raise HTTPException(
            status_code=403, 
            detail=f"权限不足: 需要 {required_permission[0]}:{required_permission[1]} 权限"
        )
    
    return {
        "message": "条件权限资源访问成功",
        "resource_id": resource_id,
        "user": current_user.username,
        "required_permission": f"{required_permission[0]}:{required_permission[1]}"
    }

# 示例6: 获取用户权限信息
@app.get("/api/user/permissions")
def get_user_permissions_info(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的权限信息"""
    permissions = auth.get_user_permissions(current_user, db)
    user_roles = [role.name for role in current_user.roles if role.is_active]
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "roles": user_roles,
        "permissions": permissions,
        "permission_count": len(permissions)
    }

# 示例7: 权限检查工具函数
def check_user_can_access_resource(user, resource_type, resource_id, db):
    """检查用户是否可以访问特定资源"""
    # 基础权限检查
    if not auth.has_permission(user, resource_type, "read", db):
        return False
    
    # 可以添加更复杂的业务逻辑
    # 例如：检查用户是否是该资源的所有者
    # 或者检查资源是否属于用户有权限的组织等
    
    return True

@app.get("/api/business/resource/{resource_id}")
def business_resource(
    resource_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """业务逻辑权限检查示例"""
    if not check_user_can_access_resource(current_user, "business", resource_id, db):
        raise HTTPException(status_code=403, detail="无法访问此资源")
    
    return {
        "message": "业务资源访问成功",
        "resource_id": resource_id,
        "user": current_user.username
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 