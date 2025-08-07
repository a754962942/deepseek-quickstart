from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from ..database import get_db
from .. import crud, schemas, auth
from ..auth import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """用户注册"""
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    """获取当前用户信息"""
    return current_user

@router.get("/me/permissions")
def get_my_permissions(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的权限"""
    permissions = auth.get_user_permissions(current_user, db)
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "permissions": permissions
    }

@router.post("/check-permission", response_model=schemas.PermissionCheckResponse)
def check_permission(
    permission_check: schemas.PermissionCheck,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """检查当前用户是否有特定权限"""
    has_permission = auth.has_permission(
        current_user, 
        permission_check.resource, 
        permission_check.action, 
        db
    )
    
    user_roles = [role.name for role in current_user.roles if role.is_active]
    
    return schemas.PermissionCheckResponse(
        has_permission=has_permission,
        user_id=current_user.id,
        username=current_user.username,
        roles=user_roles
    ) 