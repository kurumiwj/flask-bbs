import click
import logging
from logging.handlers import RotatingFileHandler
from flask import flash,Flask,make_response,redirect,render_template,url_for
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask.logging import default_handler
import config
import commands
import hooks
from extensions import avatars,cache,csrf,db,mail
from bbs_celery import make_celery
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
from models.user import PermissionEnum,PermissionModel,RoleModel
from models.post import BoardModel,CommentModel,PostModel
import filters

app=Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
cache.init_app(app)
db.init_app(app)
mail.init_app(app)
avatars.init_app(app)
Migrate(app,db,render_as_batch=True)
#跨域
CORS(app,resources=r"/*")
#设置日志级别
app.logger.setLevel(logging.INFO)
#将日志重定向到文件
# file_handler=logging.FileHandler("bbs.log",encoding="utf-8")
#创建RotatingFileHandler对象
file_handler=RotatingFileHandler("bbs.log",maxBytes=16384,backupCount=20)
file_handler.setLevel(logging.INFO)
#创建日志记录格式
file_formatter=logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]")
#将日志格式对象添加到handler中
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)
#取消控制台打印日志
app.logger.removeHandler(default_handler)
#日志过滤器
app.logger.addFilter(filters.StringFilter())
app.logger.info("abc-test")
app.logger.info("123-test")
#CSRF保护
csrf.init_app(app)
#构建celery
celery=make_celery(app)
#注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(media_bp)
#添加命令
app.cli.command("initdb")(commands.initdb)
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)
#添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)
#添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)

if __name__=="__main__":
	app.run(debug=True,port=3000,host="0.0.0.0")