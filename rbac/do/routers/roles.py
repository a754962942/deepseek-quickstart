from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import crud, schemas, auth

router = APIRouter(prefix="/roles", tags=["角色管理"])

@router.get("/", response_model=List[schemas.RoleResponse])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(auth.require_permission("roles", "read")),
    db: Session = Depends(get_db)
):
    """获取角色列表"""
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=schemas.RoleResponse)
def read_role(
    role_id: int,
    current_user: schemas.User = Depends(auth.require_permission("roles", "read")),
    db: Session = Depends(get_db)
):
    """根据ID获取角色"""
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    return db_role

@router.post("/", response_model=schemas.RoleResponse)
def create_role(
    role: schemas.RoleCreate,
    current_user: schemas.User = Depends(auth.require_permission("roles", "create")),
    db: Session = Depends(get_db)
):
    """创建角色"""
    # 检查角色名是否已存在
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="角色名已存在")
    
    return crud.create_role(db=db, role=role)

@router.put("/{role_id}", response_model=schemas.RoleResponse)
def update_role(
    role_id: int,
    role_update: schemas.RoleUpdate,
    current_user: schemas.User = Depends(auth.require_permission("roles", "update")),
    db: Session = Depends(get_db)
):
    """更新角色"""
    db_role = crud.update_role(db, role_id=role_id, role_update=role_update)
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    return db_role

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    current_user: schemas.User = Depends(auth.require_permission("roles", "delete")),
    db: Session = Depends(get_db)
):
    """删除角色"""
    success = crud.delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    return {"message": "角色删除成功"}

@router.post("/{role_id}/permissions")
def assign_permissions_to_role(
    role_id: int,
    permission_assignment: schemas.RolePermissionAssignment,
    current_user: schemas.User = Depends(auth.require_permission("roles", "update")),
    db: Session = Depends(get_db)
):
    """为角色分配权限"""
    db_role = crud.assign_permissions_to_role(db, role_id=role_id, permission_ids=permission_assignment.permission_ids)
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    return {"message": "权限分配成功", "role_id": role_id}

@router.get("/{role_id}/permissions")
def get_role_permissions(
    role_id: int,
    current_user: schemas.User = Depends(auth.require_permission("roles", "read")),
    db: Session = Depends(get_db)
):
    """获取角色的权限"""
    permissions = crud.get_role_permissions(db, role_id=role_id)
    return {"role_id": role_id, "permissions": permissions} 