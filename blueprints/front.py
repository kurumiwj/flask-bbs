import os
from flask import Blueprint,current_app,flash,g,jsonify,redirect,render_template,request,send_from_directory,url_for
from flask_paginate import Pagination
from werkzeug.utils import secure_filename
from models.post import BoardModel,CommentModel,PostModel
from extensions import csrf
from decorators import login_required
from forms.post import PublicCommentForm,PublicPostForm
from extensions import db
from utils import restful

bp=Blueprint("front", __name__,url_prefix="")

@bp.get("/")
def index():
	posts=PostModel.query.all()
	boards=BoardModel.query.all()
	#获取页码参数
	page=request.args.get("page",type=int,default=1)
	#获取版块参数
	board_id=request.args.get("board_id",type=int,default=0)
	#当前page下的起始位置
	start=(page-1)*current_app.config.get("PER_PAGE_COUNT")
	#当前page下的结束位置
	end=start+current_app.config.get("PER_PAGE_COUNT")
	query_obj=PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())
	#过滤帖子
	if board_id:
		query_obj=query_obj.filter_by(board_id=board_id)
	#总共帖子数量
	total=query_obj.count()
	posts=query_obj.slice(start,end)
	#分页对象
	pagination=Pagination(bs_version=4,page=page,total=total,outer_window=0,inner_window=2,alignment="center")
	context={
		"posts":posts,
		"boards":boards,
		"pagination":pagination,
		"current_board":board_id
	}
	current_app.logger.info("index页面被请求了！")
	return render_template("front/index.html",**context)

@bp.route("/post/public",methods=["GET","POST"])
@login_required
def public_post():
	if request.method=="GET":
		boards=BoardModel.query.all()
		return render_template("front/public_post.html",boards=boards)
	else:
		form=PublicPostForm()
		print(form)
		if form.validate_on_submit():
			title=form.title.data
			print(title)
			content=form.content.data
			print(content)
			board_id=form.board_id.data
			post=PostModel(title=title,content=content,board_id=board_id,author=g.user)
			print(post)
			db.session.add(post)
			db.session.commit()
			return restful.ok()
		else:
			for message in form.messages:
				print(message)
				flash(message)
			message=form.messages[0]
			return restful.params_error(message=message)

#帖子详情页
@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
	post=PostModel.query.get(post_id)
	post.read_count+=1
	db.session.commit()
	return render_template("front/post_detail.html",post=post)

#帖子评论
@bp.post("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
	form=PublicCommentForm()
	if form.validate_on_submit():
		content=form.content.data
		comment=CommentModel(content=content,post_id=post_id,author=g.user)
		db.session.add(comment)
		db.session.commit()
	else:
		for message in form.messages:
			flash(message)
	return redirect(url_for("front.post_detail",post_id=post_id))

#上传图片
@bp.post("/upload/image")
@csrf.exempt
@login_required
def upload_image():
	print(request.files)
	f=request.files.get("wangeditor-uploaded-image")
	extension=f.filename.split(".")[-1].lower()
	if extension not in ["jpg","jpeg","png","gif"]:
		return jsonify({
			"errno":400,
			"data":[]
		})
	filename=secure_filename(f.filename)
	f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"),filename))
	url=url_for("media.media_file",filename=filename)
	return jsonify({
		"errno":0,
		"data":[{
			"url":url,
			"alt":"",
			"href":""
		}]
	})

