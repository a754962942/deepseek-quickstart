#!/usr/bin/env python3
"""
RBAC权限管理系统启动脚本
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """主函数"""
    print("🚀 启动RBAC权限管理系统...")
    
    try:
        # 导入并初始化数据库
        from init_data import init_database
        print("📊 初始化数据库...")
        init_database()
        
        # 导入主应用
        from main import app
        print("✅ 数据库初始化完成！")
        
        print("\n" + "="*50)
        print("🎯 RBAC权限管理系统已启动")
        print("="*50)
        print("📍 访问地址: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        print("📖 ReDoc文档: http://localhost:8000/redoc")
        print("🔐 默认管理员账号: admin")
        print("🔑 默认管理员密码: admin123")
        print("="*50)
        print("⚠️  请及时修改默认密码！")
        print("="*50)
        
        # 启动服务器
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main() 