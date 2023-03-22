from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash,check_password_hash
from shortuuid import uuid
from flask_avatars import Identicon
from extensions import db

class PermissionEnum(Enum):
	BOARD="板块"
	POST="帖子"
	COMMENT="评论"
	FRONT_USER="前台用户"
	CMS_USER="后台用户"

role_permission_table=db.Table(
	"role_permission_table",
	db.Column("role_id",db.Integer,db.ForeignKey("role.id")),
	db.Column("permission_id",db.Integer,db.ForeignKey("permission.id"))
)

#权限
class PermissionModel(db.Model):
	__tablename__="permission"
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	name=db.Column(db.Enum(PermissionEnum),nullable=False,unique=True)

	roles=db.relationship("RoleModel",secondary=role_permission_table,back_populates="permissions")

#角色
class RoleModel(db.Model):
	__tablename__="role"
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	name=db.Column(db.String(50),nullable=False)
	desc=db.Column(db.String(200),nullable=True)
	create_time=db.Column(db.DateTime,default=datetime.now)

	permissions=db.relationship("PermissionModel",secondary=role_permission_table,back_populates="roles")
	users=db.relationship("UserModel",back_populates="role")

#用户
class UserModel(db.Model):
	__tablename__="user"
	id=db.Column(db.String(100),primary_key=True,default=uuid)
	username=db.Column(db.String(50),nullable=False,unique=True)
	_password=db.Column(db.String(200),nullable=False)
	email=db.Column(db.String(50),nullable=False,unique=True)
	avatar=db.Column(db.String(100))
	signature=db.Column(db.String(100))
	join_time=db.Column(db.DateTime,default=datetime.now)
	is_staff=db.Column(db.Boolean,default=False)
	is_active=db.Column(db.Boolean,default=True)
	#外键
	role_id=db.Column(db.Integer,db.ForeignKey("role.id"))

	role=db.relationship("RoleModel",back_populates="users",uselist=False)
	posts=db.relationship("PostModel",back_populates="author")

	def __init__(self,*args,**kwargs):
		if "password" in kwargs:
			self.password=kwargs.get("password")
			kwargs.pop("password")
		super(UserModel, self).__init__(*args,**kwargs)
		#generate_avatar()

	'''
	def generate_avatar(self):
		avatar=Identicon()
		filenames=avatar.generate(text=self.email)
		self.avatar_s=filenames[0]
		self.avatar_m=filenames[1]
		self.avatar_l=filenames[2]
		db.session.commit()
	'''

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self,raw_password):
		self._password=generate_password_hash(raw_password)

	def check_password(self,raw_password):
		return check_password_hash(self.password, raw_password)

	def has_permission(self,permission):
		return permission in [permission.name for permission in self.role.permissions]

