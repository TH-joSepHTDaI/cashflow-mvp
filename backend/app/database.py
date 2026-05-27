"""
数据库配置模块

提供 SQLite 数据库连接和会话管理
"""

from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

# ============================================
# 数据库配置
# ============================================

# 数据库文件路径：backend/data/cashflow.db
DATABASE_PATH = Path(__file__).parent.parent / "data" / "cashflow.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# 创建数据库引擎
# - echo=False: 关闭 SQL 语句日志（生产环境）
# - echo=True:  开启 SQL 语句日志（调试用）
# - check_same_thread=False: SQLite 必需，允许多线程访问
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 设为 True 可查看执行的 SQL 语句
    connect_args={"check_same_thread": False}
)


# ============================================
# 数据库操作函数
# ============================================

def create_db_and_tables():
    """
    创建所有数据库表
    
    根据 models.py 中定义的模型自动创建对应的表
    如果表已存在则不会重复创建
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    获取数据库会话（生成器）
    
    使用方式：
        @router.post("/")
        def create_item(session: Session = Depends(get_session)):
            ...
    
    自动管理会话生命周期，确保连接正确关闭
    """
    with Session(engine) as session:
        yield session
