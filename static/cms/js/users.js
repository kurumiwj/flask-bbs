$(function(){
	$(".active-btn").click(function(e){
		e.preventDefault();
		let $this=$(this);
		let isActive=parseInt($this.attr("data-active"));
		let message=isActive ? "您确定要禁用此用户吗？" : "您确定要取消禁用此用户吗？";
		let userId=$this.attr("data-user-id");
		let result=confirm(message);
		if(!result){
			return ;
		}
		let data={
			is_active:isActive ? 0 : 1
		}
		zlajax.post({
			url:"/cms/users/active/"+userId,
			data
		}).done(function(){
			window.location.reload();
		}).fail(function(error){
			alert(error.message);
		});
	});
});