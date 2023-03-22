$(function(){
	const {createEditor,createToolbar}=window.wangEditor;
	let content="";
	const editorConfig = {
    placeholder: 'Type here...',
		MENU_CONF:{
			uploadImage:{
				server:"/upload/image",
				maxFileSize:10*1024*1024
			}
		},
    onChange(editor) {
      const html = editor.getHtml();
			content=editor.getText();
      console.log('editor content', html);
    }
	}
	const editor = createEditor({
		selector: '#editor',
		html: '<p><br></p>',
		config: editorConfig,
		mode: 'default', // or 'simple'
	});
	const toolbarConfig = {}
	const toolbar = createToolbar({
		editor,
		selector: '#toolbar',
		config: toolbarConfig,
		mode: 'default', // or 'simple'
	});
	
	//提交按钮单击事件
	$("#submit-btn").click(function(event){
		event.preventDefault();
		let title=$("input[name='title']").val();
		let board_id=$("select[name='board_id']").val();
		zlajax.post({
			url:"/post/public",
			data:{title,board_id,content}
		}).done(function(data){
			setTimeout(function(){
				window.location="/";
			},2000);
		}).fail(function(error){
			alert(error.message);
		});
	})
});