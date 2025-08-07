from sqlalchemy.orm import Session
from .database import SessionLocal, create_tables
from . import crud, schemas, auth
from .models import User, Role, Permission

def init_database():
    """初始化数据库"""
    # 创建表
    create_tables()
    
    # 获取数据库会话
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_users = crud.get_users(db, limit=1)
        if existing_users:
            print("数据库已存在数据，跳过初始化")
            return
        
        print("开始初始化数据库...")
        
        # 创建基础权限
        permissions_data = [
            # 用户管理权限
            {"name": "用户查看", "resource": "users", "action": "read", "description": "查看用户列表和详情"},
            {"name": "用户创建", "resource": "users", "action": "create", "description": "创建新用户"},
            {"name": "用户更新", "resource": "users", "action": "update", "description": "更新用户信息"},
            {"name": "用户删除", "resource": "users", "action": "delete", "description": "删除用户"},
            
            # 角色管理权限
            {"name": "角色查看", "resource": "roles", "action": "read", "description": "查看角色列表和详情"},
            {"name": "角色创建", "resource": "roles", "action": "create", "description": "创建新角色"},
            {"name": "角色更新", "resource": "roles", "action": "update", "description": "更新角色信息"},
            {"name": "角色删除", "resource": "roles", "action": "delete", "description": "删除角色"},
            
            # 权限管理权限
            {"name": "权限查看", "resource": "permissions", "action": "read", "description": "查看权限列表和详情"},
            {"name": "权限创建", "resource": "permissions", "action": "create", "description": "创建新权限"},
            {"name": "权限更新", "resource": "permissions", "action": "update", "description": "更新权限信息"},
            {"name": "权限删除", "resource": "permissions", "action": "delete", "description": "删除权限"},
            
            # 系统管理权限
            {"name": "系统查看", "resource": "system", "action": "read", "description": "查看系统信息"},
            {"name": "系统管理", "resource": "system", "action": "manage", "description": "管理系统设置"},
        ]
        
        permissions = []
        for perm_data in permissions_data:
            permission = crud.create_permission(db, schemas.PermissionCreate(**perm_data))
            permissions.append(permission)
            print(f"创建权限: {permission.name}")
        
        # 创建基础角色
        roles_data = [
            {
                "name": "超级管理员",
                "description": "拥有所有权限的超级管理员角色",
                "permissions": [perm.id for perm in permissions]  # 所有权限
            },
            {
                "name": "管理员",
                "description": "系统管理员角色",
                "permissions": [perm.id for perm in permissions if perm.resource != "system" or perm.action != "manage"]
            },
            {
                "name": "用户管理员",
                "description": "用户管理角色",
                "permissions": [perm.id for perm in permissions if perm.resource == "users"]
            },
            {
                "name": "角色管理员",
                "description": "角色管理角色",
                "permissions": [perm.id for perm in permissions if perm.resource == "roles"]
            },
            {
                "name": "权限管理员",
                "description": "权限管理角色",
                "permissions": [perm.id for perm in permissions if perm.resource == "permissions"]
            },
            {
                "name": "普通用户",
                "description": "普通用户角色",
                "permissions": []  # 无特殊权限
            }
        ]
        
        roles = []
        for role_data in roles_data:
            role_permissions = role_data.pop("permissions")
            role = crud.create_role(db, schemas.RoleCreate(**role_data))
            if role_permissions:
                crud.assign_permissions_to_role(db, role.id, role_permissions)
            roles.append(role)
            print(f"创建角色: {role.name}")
        
        # 创建管理员用户
        admin_user = crud.create_user(db, schemas.UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123"
        ))
        
        # 为管理员分配超级管理员角色
        super_admin_role = next(role for role in roles if role.name == "超级管理员")
        crud.assign_roles_to_user(db, admin_user.id, [super_admin_role.id])
        
        print(f"创建管理员用户: {admin_user.username}")
        print("数据库初始化完成！")
        print(f"管理员账号: {admin_user.username}")
        print(f"管理员密码: admin123")
        print("请及时修改默认密码！")
        
    except Exception as e:
        print(f"初始化数据库时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 