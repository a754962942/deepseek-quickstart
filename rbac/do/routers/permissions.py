from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import crud, schemas, auth

router = APIRouter(prefix="/permissions", tags=["权限管理"])

@router.get("/", response_model=List[schemas.PermissionResponse])
def read_permissions(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "read")),
    db: Session = Depends(get_db)
):
    """获取权限列表"""
    permissions = crud.get_permissions(db, skip=skip, limit=limit)
    return permissions

@router.get("/{permission_id}", response_model=schemas.PermissionResponse)
def read_permission(
    permission_id: int,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "read")),
    db: Session = Depends(get_db)
):
    """根据ID获取权限"""
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="权限不存在")
    return db_permission

@router.get("/resource/{resource}", response_model=List[schemas.PermissionResponse])
def read_permissions_by_resource(
    resource: str,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "read")),
    db: Session = Depends(get_db)
):
    """根据资源获取权限"""
    permissions = crud.get_permissions_by_resource(db, resource=resource)
    return permissions

@router.post("/", response_model=schemas.PermissionResponse)
def create_permission(
    permission: schemas.PermissionCreate,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "create")),
    db: Session = Depends(get_db)
):
    """创建权限"""
    # 检查权限名是否已存在
    db_permission = crud.get_permission_by_name(db, name=permission.name)
    if db_permission:
        raise HTTPException(status_code=400, detail="权限名已存在")
    
    return crud.create_permission(db=db, permission=permission)

@router.put("/{permission_id}", response_model=schemas.PermissionResponse)
def update_permission(
    permission_id: int,
    permission_update: schemas.PermissionUpdate,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "update")),
    db: Session = Depends(get_db)
):
    """更新权限"""
    db_permission = crud.update_permission(db, permission_id=permission_id, permission_update=permission_update)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="权限不存在")
    return db_permission

@router.delete("/{permission_id}")
def delete_permission(
    permission_id: int,
    current_user: schemas.User = Depends(auth.require_permission("permissions", "delete")),
    db: Session = Depends(get_db)
):
    """删除权限"""
    success = crud.delete_permission(db, permission_id=permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="权限不存在")
    return {"message": "权限删除成功"} 