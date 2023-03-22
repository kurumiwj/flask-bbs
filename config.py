import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY="kurumi"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #设置session过期时间
    PERMANENT_SESSION_LIFETIME=timedelta(days=90)
    #设置每页展示多少条数据
    PER_PAGE_COUNT=10
    UPLOAD_IMAGE_PATH=os.path.join(os.path.dirname(__file__),"media")

class DevelopmentConfig(BaseConfig):
    #数据库配置
    host="127.0.0.1"
    port=3306
    username="root"
    password="123456"
    database="bbs"
    SQLALCHEMY_DATABASE_URI="sqlite:///D:/Study/flask/3/07-project/data.db"
    #邮箱配置
    MAIL_SERVER="smtp.126.com"
    MAIL_USE_SSL=True
    MAIL_PORT=465
    MAIL_USERNAME="zhuwenjienet@126.com"
    MAIL_PASSWORD="KZUVUUBBLAPIDOHG"
    MAIL_DEFAULT_SENDER="zhuwenjienet@126.com"
    #缓存配置
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST="127.0.0.1"
    CACHE_REDIS_PORT="6379"
    #Celery配置
    #格式:redis://:password@hostname:port/db_number
    CELERY_BROKER_URL="redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/0"
    #头像路径
    AVATARS_SAVE_PATH=os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")
    #本地服务器图片路径
    LOCAL_IMAGE_URL="http://localhost:1002/images/"
