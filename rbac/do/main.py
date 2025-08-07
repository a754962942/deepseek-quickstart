from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import uvicorn

from .database import get_db, create_tables
from .routers import auth, users, roles, permissions
from . import crud, schemas, auth as auth_module

# 创建FastAPI应用
app = FastAPI(
    title="RBAC权限管理系统",
    description="基于FastAPI的RBAC（基于角色的访问控制）权限管理系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(permissions.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """应用启动时创建数据库表"""
    create_tables()

@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "RBAC权限管理系统API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.get("/api/v1/system/info")
def get_system_info(
    current_user: schemas.User = Depends(auth_module.require_permission("system", "read")),
    db: Session = Depends(get_db)
):
    """获取系统信息（需要system:read权限）"""
    return {
        "system_name": "RBAC权限管理系统",
        "version": "1.0.0",
        "current_user": current_user.username,
        "user_permissions": auth_module.get_user_permissions(current_user, db)
    }

@app.post("/api/v1/system/check-permission")
def check_system_permission(
    permission_check: schemas.PermissionCheck,
    current_user: schemas.User = Depends(auth_module.get_current_active_user),
    db: Session = Depends(get_db)
):
    """检查系统权限（公开接口，但需要登录）"""
    has_permission = auth_module.has_permission(
        current_user, 
        permission_check.resource, 
        permission_check.action, 
        db
    )
    
    return {
        "has_permission": has_permission,
        "user_id": current_user.id,
        "username": current_user.username,
        "resource": permission_check.resource,
        "action": permission_check.action
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 