from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 基础模式
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# 用户相关模式
class UserBase(BaseSchema):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    roles: List['RoleResponse'] = []

# 角色相关模式
class RoleBase(BaseSchema):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class RoleResponse(RoleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    permissions: List['PermissionResponse'] = []

# 权限相关模式
class PermissionBase(BaseSchema):
    name: str
    resource: str
    action: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseSchema):
    name: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class PermissionResponse(PermissionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

# 认证相关模式
class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    username: Optional[str] = None

class LoginRequest(BaseSchema):
    username: str
    password: str

# 用户角色分配模式
class UserRoleAssignment(BaseSchema):
    user_id: int
    role_ids: List[int]

class RolePermissionAssignment(BaseSchema):
    role_id: int
    permission_ids: List[int]

# 权限检查模式
class PermissionCheck(BaseSchema):
    resource: str
    action: str

class PermissionCheckResponse(BaseSchema):
    has_permission: bool
    user_id: int
    username: str
    roles: List[str]

# 更新前向引用
UserResponse.model_rebuild()
RoleResponse.model_rebuild()
PermissionResponse.model_rebuild() 