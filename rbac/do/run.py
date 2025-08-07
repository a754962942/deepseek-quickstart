#!/usr/bin/env python3
"""
RBAC权限管理系统启动脚本
"""

import uvicorn
from .main import app
from .init_data import init_database

def main():
    """主函数"""
    print("正在初始化RBAC权限管理系统...")
    
    # 初始化数据库
    init_database()
    
    print("启动RBAC权限管理系统服务器...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("ReDoc文档: http://localhost:8000/redoc")
    
    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 