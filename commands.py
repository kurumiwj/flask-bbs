import click
import random
from faker import Faker
from extensions import db
from models.user import PermissionEnum,PermissionModel,RoleModel,UserModel
from models.post import BoardModel,PostModel

#初始化数据库命令
@click.option("--drop",is_flag=True,help="Create database after Drop!")
def initdb(drop):
	if drop:
		click.confirm("This operation will delete the database,do you want to continue?",abort=True)
		db.drop_all()
		click.echo("Drop tables!")
	db.create_all()
	click.echo("Initialized database!")

#添加权限命令
def create_permission():
	for permissionName in dir(PermissionEnum):
		if permissionName.startswith("__"):
			continue
		permission=PermissionModel(name=getattr(PermissionEnum,permissionName))
		db.session.add(permission)
	db.session.commit()
	click.echo("权限添加成功！")

#添加角色命令
def create_role():
	#稽查
	inspector=RoleModel(name="稽查",desc="负责审核帖子和评论是否合法合规！")
	inspector.permissions=PermissionModel.query.filter(PermissionModel.name.in_([PermissionEnum.POST,PermissionEnum.COMMENT])).all()
	#运营
	operator=RoleModel(name="运营",desc="负责网站持续正常运营！")
	operator.permissions=PermissionModel.query.filter(PermissionModel.name.in_([PermissionEnum.POST,PermissionEnum.COMMENT,PermissionEnum.BOARD,PermissionEnum.FRONT_USER,PermissionEnum.CMS_USER])).all()
	#管理员
	administrator=RoleModel(name="管理员",desc="负责整个网站所有工作！")
	administrator.permissions=PermissionModel.query.all()

	db.session.add_all([inspector,operator,administrator])
	db.session.commit()
	click.echo("角色添加成功！")

#创建测试用户
def create_test_user():
	admin_role=RoleModel.query.filter_by(name="管理员").first()
	admin=UserModel(username="admin",email="admin@126.com",password="123456",is_staff=True,role=admin_role)

	operator_role=RoleModel.query.filter_by(name="运营").first()
	operator=UserModel(username="operator",email="operator@126.com",password="123456",is_staff=True,role=operator_role)

	inspector_role=RoleModel.query.filter_by(name="稽查").first()
	inspector=UserModel(username="inspector",email="inspector@126.com",password="123456",is_staff=True,role=inspector_role)

	db.session.add_all([admin,operator,inspector])
	db.session.commit()
	click.echo("测试用户添加成功！")

#创建管理员
@click.option("--username","-u")
@click.option("--email","-e")
@click.option("--password","-p")
def create_admin(username,email,password):
	admin_role=RoleModel.query.filter_by(name="管理员").first()
	admin_user=UserModel(username=username,email=email,password=password,is_staff=True,role=admin_role)
	db.session.add(admin_user)
	db.session.commit()
	click.echo("创建管理员成功！")

#添加板块
def create_board():
	board_names=["Python","Java","Rust","GO","C++"]
	for name in board_names:
		board=BoardModel(name=name)
		db.session.add(board)
	db.session.commit()
	click.echo("板块添加成功！")

#生成帖子测试数据
def create_test_post():
	fake=Faker(locale="zh_CN")
	author=UserModel.query.first()
	boards=BoardModel.query.all()
	click.echo("开始生成测试帖子")
	for x in range(98):
		title=fake.sentence()
		content=fake.paragraph(nb_sentences=10)
		random_index=random.randint(0,4)
		board=boards[random_index]
		post=PostModel(title=title,content=content,board=board,author=author)
		db.session.add(post)
	db.session.commit()
	click.echo("测试帖子生成成功！")