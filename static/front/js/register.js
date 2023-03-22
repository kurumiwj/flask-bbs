$(function(){
	$("#captcha-btn").on("click",function(event){
		event.preventDefault();
		//获取邮箱
		let email=$("input[name='email']").val();
		zlajax.get({
			url:"/user/mail/captcha?mail="+email
		}).done(function(result){
			alert("验证码发送成功！");
		}).fail(function(error){
			alert(error.message);
		});
	});
});