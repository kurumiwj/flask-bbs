$(function(){
	$(".active-btn").click(function(e){
		e.preventDefault();
		let $this=$(this);
		let isActive=parseInt($this.attr("data-active"));
		let message=isActive ? "您确定要隐藏此帖子吗？" : "您确定要显示此帖子吗？";
		let postId=$this.attr("data-post-id");
		let result=confirm(message);
		if(!result){
			return ;
		}
		let data={
			is_active:isActive ? 0 : 1
		}
		zlajax.post({
			url:"/cms/posts/active/"+postId,
			data
		}).done(function(){
			window.location.reload();
		}).fail(function(error){
			alert(error.message);
		});
	});
});