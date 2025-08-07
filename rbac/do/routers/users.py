from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import crud, schemas, auth

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(auth.require_permission("users", "read")),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: int,
    current_user: schemas.User = Depends(auth.require_permission("users", "read")),
    db: Session = Depends(get_db)
):
    """根据ID获取用户"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    current_user: schemas.User = Depends(auth.require_permission("users", "create")),
    db: Session = Depends(get_db)
):
    """创建用户"""
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    return crud.create_user(db=db, user=user)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: schemas.User = Depends(auth.require_permission("users", "update")),
    db: Session = Depends(get_db)
):
    """更新用户"""
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: schemas.User = Depends(auth.require_permission("users", "delete")),
    db: Session = Depends(get_db)
):
    """删除用户"""
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}

@router.post("/{user_id}/roles")
def assign_roles_to_user(
    user_id: int,
    role_assignment: schemas.UserRoleAssignment,
    current_user: schemas.User = Depends(auth.require_permission("users", "update")),
    db: Session = Depends(get_db)
):
    """为用户分配角色"""
    db_user = crud.assign_roles_to_user(db, user_id=user_id, role_ids=role_assignment.role_ids)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "角色分配成功", "user_id": user_id}

@router.get("/{user_id}/roles")
def get_user_roles(
    user_id: int,
    current_user: schemas.User = Depends(auth.require_permission("users", "read")),
    db: Session = Depends(get_db)
):
    """获取用户的角色"""
    roles = crud.get_user_roles(db, user_id=user_id)
    return {"user_id": user_id, "roles": roles} 