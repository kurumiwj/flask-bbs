from flask import Blueprint,current_app,g,redirect,render_template,request
from flask_paginate import Pagination
from models.user import PermissionEnum,RoleModel,UserModel
from models.post import BoardModel,CommentModel,PostModel
from decorators import permission_required
from forms.cms import AddStaffForm,EditBoardForm,EditStaffForm
from utils import restful
from extensions import db

bp=Blueprint("cms", __name__,url_prefix="/cms")

#判断当前用户是否是员工
@bp.before_request
def cms_before_request():
	if not hasattr(g,"user") or g.user.is_staff==False:
		return redirect("/")

#将PermissionEnum传给模板
@bp.context_processor
def cms_context_processor():
	return {"PermissionEnum":PermissionEnum}

@bp.get("")
def index():
	return render_template("cms/index.html")

@bp.get("/staff/list")
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
	users=UserModel.query.filter_by(is_staff=True).all()
	return render_template("cms/staff_list.html",users=users)

#添加员工
@bp.route("/staff/add",methods=["GET","POST"])
@permission_required(PermissionEnum.CMS_USER)
def add_staff():
	if request.method=="GET":
		roles=RoleModel.query.all()
		return render_template("cms/add_staff.html",roles=roles)
	else:
		form=AddStaffForm()
		if form.validate_on_submit():
			email=form.email.data
			role_id=form.role.data
			user=UserModel.query.filter_by(email=email).first()
			if not user:
				flash("没有此用户！")
				return redirect(url_for("cms.add_staff"))
			user.is_staff=True
			user.role=RoleModel.query.get(role_id)
			db.session.commit()
			return redirect(url_for("cms.staff_list"))

#编辑员工
@bp.route("/staff/edit/<string:user_id>",methods=["GET","POST"])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff(user_id):
	user=UserModel.query.get(user_id)
	if request.method=="GET":
		roles=RoleModel.query.all()
		return render_template("cms/edit_staff.html",user=user,roles=roles)
	else:
		form=EditStaffForm()
		if form.validate_on_submit():
			is_staff=form.is_staff.data
			role_id=form.role.data
			user.is_staff=is_staff
			if user.role.id!=role_id:
				user.role=RoleModel.query.get(role_id)
			db.session.commit()
			return redirect(url_for("cms.edit_staff",user_id=user_id))
		else:
			for message in form.messages:
				flash(message)
			return redirect(url_for("cms.edit_staff",user_id=user_id))

#返回用户列表
@bp.get("/users")
@permission_required(PermissionEnum.FRONT_USER)
def user_list():
	users=UserModel.query.filter_by(is_staff=False).all()
	return render_template("cms/users.html",users=users)

@bp.post("/users/active/<string:user_id>")
@permission_required(PermissionEnum.FRONT_USER)
def active_user(user_id):
	is_active=request.form.get("is_active",type=int)
	if is_active==None:
		return restful.params_error(message="请传入is_active参数！")
	user=UserModel.query.get(user_id)
	user.is_active=bool(is_active)
	db.session.commit()
	return restful.ok()

#帖子管理
@bp.get("/posts")
@permission_required(PermissionEnum.POST)
def post_list():
	page=request.args.get("page",type=int,default=1)
	start=(page-1)*current_app.config.get("PER_PAGE_COUNT")
	end=start+current_app.config.get("PER_PAGE_COUNT")
	query_obj=PostModel.query.order_by(PostModel.create_time.desc())
	total=query_obj.count()
	posts=query_obj.slice(start,end)
	pagination=Pagination(bs_version=4,page=page,total=total,outer_window=0,inner_window=2,alignment="center")
	context={
		"posts":posts,
		"pagination":pagination,
	}
	return render_template("cms/posts.html",**context)

@bp.post("/posts/active/<int:post_id>")
@permission_required(PermissionEnum.POST)
def active_post(post_id):
	is_active=request.form.get("is_active",type=int)
	if is_active==None:
		return restful.params_error(message="请传入is_active参数！")
	post=PostModel.query.get(post_id)
	post.is_active=bool(is_active)
	db.session.commit()
	return restful.ok()

#评论管理
@bp.get("/comments")
@permission_required(PermissionEnum.COMMENT)
def comment_list():
	page=request.args.get("page",type=int,default=1)
	start=(page-1)*current_app.config.get("PER_PAGE_COUNT")
	end=start+current_app.config.get("PER_PAGE_COUNT")
	query_obj=CommentModel.query.order_by(CommentModel.create_time.desc())
	total=query_obj.count()
	comments=query_obj.slice(start,end)
	pagination=Pagination(bs_version=4,page=page,total=total,outer_window=0,inner_window=2,alignment="center")
	context={
		"comments":comments,
		"pagination":pagination
	}
	return render_template("cms/comments.html",**context)

@bp.post("/comments/active/<int:comment_id>")
@permission_required(PermissionEnum.COMMENT)
def active_comment(comment_id):
	is_active=request.form.get("is_active",type=int)
	if is_active==None:
		return restful.params_error(message="请传入is_active参数！")
	comment=CommentModel.query.get(comment_id)
	comment.is_active=bool(is_active)
	db.session.commit()
	return restful.ok()

#板块管理
@bp.get("/boards")
@permission_required(PermissionEnum.BOARD)
def board_list():
	boards=BoardModel.query.all()
	page=request.args.get("page",type=int,default=1)
	start=(page-1)*current_app.config.get("PER_PAGE_COUNT")
	end=start+current_app.config.get("PER_PAGE_COUNT")
	total=len(boards)
	pagination=Pagination(bs_version=4,page=page,total=total,outer_window=0,inner_window=2,alignment="center")
	context={
		"boards":boards,
		"pagination":pagination
	}
	return render_template("cms/boards.html",**context)

@bp.get("/boards/edit")
@permission_required(PermissionEnum.BOARD)
def edit_board():
	form=EditBoardForm()
	if form.validate_on_submit():
		board_id=form.board_id.data
		name=form.name.data
		board=BoardModel.query.get(board_id)
		board.name=name
		db.session.commit()
		return restful.ok()
	else:
		return restful.params_error(form.message[0])

@bp.delete("/boards/active/<int:board_id>")
@permission_required(PermissionEnum.BOARD)
def active_board(board_id):
	is_active=request.form.get("is_active",type=int)
	if is_active==None:
		return restful.params_error("请传入is_active参数！")
	board=BoardModel.query.get(board_id)
	board.is_active=bool(is_active)
	db.session.commit()
	return restful.ok()


