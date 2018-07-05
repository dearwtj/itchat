一、基础环境

    python2.7

二、项目说明

    基于flask和itchat，提供api用于发送微信消息
    场景：
            第三方调用api   ->   flask接收请求   ->  flask请求过滤，调用itchat  ->   itchat发送微信消息


三、依赖包安装

    详细依赖包清单，以及依赖包的版本信息，请查看文件‘requirements.txt’
    可通过 pip install -r requirements.txt   安装项目依赖的包

四、安装项目需手动配置
    base.py文件：    
               LOG_ROOT_DIRECTORY = 'F:\\python_logging'     #设置日志文件根目录
    flask_api.py文件：  
                     ALLOWED_UPLOAD_FILE_TYPE = ['pdf','jpg','png','docx']      #上传文件，支持的文件后缀
                     UPLOAD_FILE_PATH = 'F:\python_file_upload'       #文件上传的路劲
            
            
            
            
五、其他
   5.1  发送消息给好友 /api/sendTextMessageToFriend
   post提交json数据
   {"nickname":"微信好友昵称","sendcontent":"发送内容"}
   
   5.2  发消息到群 /api/sendTextMessageToChatRoom
   post提交json数据
   {"nickname":"群备注","sendcontent":"发送内容"}
   
   5.3  单个文件上传/api/uploadFile
   post提交form表单
   
   5.4  多个文件上传/api/uploadFiles、
   post提交form表单
   
   5.5  发送文件给好友或者群/api/sendFilesToFriendOrChatroom
   post提交json数据
   {"fileName":["文件1","文件2"],"friendNickName":"好友昵称","chatroomNickName":"群备注"}
   
   5.6  发送文本或者文件给好友或者群/api/sendTextOrFileToFriendOrChatroom
   post提交json数据
   {
	"friendNickName": ["好友昵称","好友昵称"],
	"chatroomNickName": ["群备注","群备注"],
	"files":[{"sendFriend":true,"sendChatroom":true,"fileNames":["文件名","文件名"]}],
	"content":[{"sendFriend":true,"sendChatroom":true,"content":"发送的文本"}]
  }
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
