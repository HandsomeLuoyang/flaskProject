from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config():
    """配置参数"""
    # 链接数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:tlh078797@118.31.245.241/test_road_1'

    # 数据库中表的格式修改，模型同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = 'CQJTU'

    # WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = 'CQJTU'

    # 查询显示原始sql语句
    # SQLALCHEMY_ECHO = True
