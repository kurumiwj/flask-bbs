$(function(){
	$(".active-btn").click(function(e){
		e.preventDefault();
		let $this=$(this);
		let isActive=parseInt($this.attr("data-active"));
		let message=isActive ? "确定要隐藏该条评论吗？" : "确定要显示该条评论吗？";
		let commentId=$this.attr("data-comment-id");
		let result=confirm(message);
		if(!result){
			return ;
		}
		let data={
			is_active:isActive ? 0 : 1
		}
		zlajax.post({
			url:"/cms/comments/active/"+commentId,
			data
		}).done(function(){
			window.location.reload();
		}).fail(function(error){
			alert(error.message);
		});
	});
});