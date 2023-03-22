from .base import BaseForm
from wtforms import BooleanField,IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length

#添加员工
class AddStaffForm(BaseForm):
	email=StringField(validators=[Email(message="请输入正确格式的邮箱！")])
	role=IntegerField(validators=[InputRequired(message="请选择角色！")])

#编辑员工
class EditStaffForm(BaseForm):
	is_staff=BooleanField(validators=[InputRequired(message="请选择是否是员工！")])
	role=IntegerField(validators=[InputRequired(message="请选择分组！")])

#编辑板块
class EditBoardForm(BaseForm):
	board_id=IntegerField(validators=[InputRequired(message="请输入板块id！")])
	name=StringField(validators=[Length(min=1,max=20,message="请输入1~20位长度")])

