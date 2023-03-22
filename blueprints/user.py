import os
import random
from flask import Blueprint,current_app,flash,g,redirect,render_template,request,send_from_directory,session,url_for
from flask_mail import Message
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from extensions import cache,db,mail
from utils import restful
from forms.user import EditProfileForm,LoginForm,RegisterForm
from models.user import UserModel
from decorators import login_required

bp=Blueprint("user", __name__,url_prefix="/user")

#注册
@bp.route("/register",methods=["GET","POST"])
def register():
	if request.method=="GET":
		return render_template("front/register.html")
	else:
		form=RegisterForm()
		if form.validate_on_submit():
			email=form.email.data
			username=form.username.data
			password=form.password.data
			user=UserModel(username=username,email=email,password=password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for("user.login"))
		else:
			for message in form.messages:
				flash(message)
			return redirect(url_for("user.register"))

#邮箱验证码
@bp.route("/mail/captcha")
def mail_captcha():
	try:
		email=request.args.get("mail")
		#email="zhuwenjienet@163.com"
		digits=['0','1','2','3','4','5','6','7','8','9']
		captcha="".join(random.sample(digits,4))
		subject="【Python论坛】注册验证码"
		body=f"【Python论坛】您的注册验证码是：{captcha}，请勿告诉他人！"
		current_app.celery.send_task("send_mail",(email,subject,body))
		#message=Message(subject="主题",recipients=[email],body=body)
		#mail.send(message)
		cache.set(email,captcha,timeout=300)
		return restful.ok(message="邮件发送成功！")
	except Exception as e:
		print(e)
		return restful.server_error()

#登录
@bp.route("/login",methods=["GET","POST"])
def login():
	if request.method=="GET":
		return render_template("front/login.html")
	else:
		form=LoginForm()
		if form.validate_on_submit():
			email=form.email.data
			password=form.password.data
			remember=form.remember.data
			user=UserModel.query.filter_by(email=email).first()
			if user and user.check_password(password):
				if not user.is_active:
					flash("该用户已被禁用！")
					return redirect(url_for("user.login"))
				session["user_id"]=user.id
				if remember:
					session.permanent=True
				return redirect("/")
			else:
				flash("邮箱或者密码错误！")
				return redirect(url_for("user.login"))
		else:
			for message in form.messages:
				flash(message)
			return render_template("front/login.html")

#个人中心
@bp.get("/profile/<string:user_id>")
def profile(user_id):
	user=UserModel.query.get(user_id)
	#判断是否是自己的个人中心
	is_mine=False
	if hasattr(g,"user") and g.user.id==user_id:
		is_mine=True
	context={
		"user":user,
		"is_mine":is_mine
    }
	return render_template("front/profile.html",**context)

#编辑个人中心
@bp.post("/profile/edit")
@login_required
def edit_profile():
	form=EditProfileForm(CombinedMultiDict([request.form,request.files]))
	if form.validate_on_submit():
		username=form.username.data
		avatar=form.avatar.data
		signature=form.signature.data
		#如果上传了头像
		if avatar:
			#生成安全的文件名
			filename=secure_filename(avatar.filename)
			#拼接头像存储路径
			avatar_path=os.path.join(current_app.config.get("AVATARS_SAVE_PATH"),filename)
			#保存文件
			avatar.save(avatar_path)
			#设置头像URL
			#g.user.avatar=url_for("media.media_file",filename=os.path.join("avatars",filename))
			g.user.avatar=current_app.config.get("LOCAL_IMAGE_URL")+filename
			print(g.user.avatar)
		g.user.username=username
		g.user.signature=signature
		db.session.commit()
		return redirect(url_for("user.profile",user_id=g.user.id))
	else:
		for message in form.messages:
			flash(message)
		return redirect(url_for("user.profile",user_id=g.user.id))

#退出登录
@bp.get("/logout")
def logout():
	session.clear()
	return redirect("/")