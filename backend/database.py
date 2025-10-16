from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接 URL (请根据您的 Laragon MySQL 设置修改)
# 格式: "mysql+pymysql://<user>:<password>@<host>/<dbname>"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/blue_local_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()