from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash

# 用户相关CRUD操作
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """根据ID获取用户"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """根据用户名获取用户"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """根据邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """获取用户列表"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """创建用户"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """更新用户"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """删除用户"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# 角色相关CRUD操作
def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    """根据ID获取角色"""
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, name: str) -> Optional[models.Role]:
    """根据名称获取角色"""
    return db.query(models.Role).filter(models.Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Role]:
    """获取角色列表"""
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    """创建角色"""
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_update: schemas.RoleUpdate) -> Optional[models.Role]:
    """更新角色"""
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    
    update_data = role_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    """删除角色"""
    db_role = get_role(db, role_id)
    if not db_role:
        return False
    
    db.delete(db_role)
    db.commit()
    return True

# 权限相关CRUD操作
def get_permission(db: Session, permission_id: int) -> Optional[models.Permission]:
    """根据ID获取权限"""
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str) -> Optional[models.Permission]:
    """根据名称获取权限"""
    return db.query(models.Permission).filter(models.Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Permission]:
    """获取权限列表"""
    return db.query(models.Permission).offset(skip).limit(limit).all()

def get_permissions_by_resource(db: Session, resource: str) -> List[models.Permission]:
    """根据资源获取权限"""
    return db.query(models.Permission).filter(models.Permission.resource == resource).all()

def create_permission(db: Session, permission: schemas.PermissionCreate) -> models.Permission:
    """创建权限"""
    db_permission = models.Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: int, permission_update: schemas.PermissionUpdate) -> Optional[models.Permission]:
    """更新权限"""
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        return None
    
    update_data = permission_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_permission, field, value)
    
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int) -> bool:
    """删除权限"""
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        return False
    
    db.delete(db_permission)
    db.commit()
    return True

# 用户角色分配操作
def assign_roles_to_user(db: Session, user_id: int, role_ids: List[int]) -> Optional[models.User]:
    """为用户分配角色"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # 清除现有角色
    db_user.roles.clear()
    
    # 添加新角色
    for role_id in role_ids:
        role = get_role(db, role_id)
        if role:
            db_user.roles.append(role)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_roles(db: Session, user_id: int) -> List[models.Role]:
    """获取用户的角色"""
    db_user = get_user(db, user_id)
    if not db_user:
        return []
    return db_user.roles

# 角色权限分配操作
def assign_permissions_to_role(db: Session, role_id: int, permission_ids: List[int]) -> Optional[models.Role]:
    """为角色分配权限"""
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    
    # 清除现有权限
    db_role.permissions.clear()
    
    # 添加新权限
    for permission_id in permission_ids:
        permission = get_permission(db, permission_id)
        if permission:
            db_role.permissions.append(permission)
    
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role_permissions(db: Session, role_id: int) -> List[models.Permission]:
    """获取角色的权限"""
    db_role = get_role(db, role_id)
    if not db_role:
        return []
    return db_role.permissions

# 权限检查操作
def check_user_permission(db: Session, user_id: int, resource: str, action: str) -> bool:
    """检查用户是否有特定权限"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    for role in db_user.roles:
        if not role.is_active:
            continue
        for permission in role.permissions:
            if not permission.is_active:
                continue
            if permission.resource == resource and permission.action == action:
                return True
    
    return False 