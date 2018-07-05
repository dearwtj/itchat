# coding: utf-8
# Author: tingjun/wei
# Data: 2018年6月8日


import json
import os
import time


from flask import Flask
from flask import request
from flask import jsonify


from my_itchat import Itchat
from base import Enum

ALLOWED_UPLOAD_FILE_TYPE = ['pdf','jpg','png','docx']      #上传文件，支持的文件后缀
UPLOAD_FILE_PATH = 'F:\python_file_upload'       #文件上传的路劲
app = Flask(__name__)
@app.route('/api/sendTextMessageToFriend',methods = ['POST'])
def send_text_message_to_friend():      #发送消息给好友
    try:
        res_json = {"resList": [], "code": "", "resMessage": ""}   #创建返回字典{"resList": [{"type": "noString", "id": 12}], "code": "1000", "resMessage": ""}
        if request.method == "POST":
            # print request.form.get('body')
            data = json.loads(request.get_data())   #获取接口传入的json入参
            if len(data) == 0 or data is None:  #参数为空校验
                res_json["code"] = Enum.res_param_empty
                res_json["resMessage"] = "param empty"
            elif data.has_key("nickname") is False or data.has_key("sendcontent") is False: #参数缺失校验
                res_json["code"] = Enum.res_param_missing
                res_json["resMessage"] = "param missing"

            elif ic.send_message(friend_nickname=data["nickname"],content=data["sendcontent"]):
                res_json["code"] = Enum.res_success
                res_json["resMessage"] = "success"
            else:
                res_json["code"] = Enum.res_fail
                res_json["resMessage"] = "发送消息发生异常，请联系15680502703"

    except Exception as result:
        res_json["code"] = Enum.res_fail
        res_json["resMessage"] = result
    finally:
        return jsonify(res_json)

@app.route('/api/sendTextMessageToChatRoom',methods = ['POST'])
def send_text_message_to_chatroom():        #发送消息到微信群
    try:
        res_json = {"resList": [], "code": "", "resMessage": ""}   #创建返回字典{"resList": [{"type": "noString", "id": 12}], "code": "1000", "resMessage": ""}
        if request.method == "POST":
            # print request.form.get('body')
            data = json.loads(request.get_data())   #获取接口传入的json入参
            if len(data) == 0 or data is None:  #参数为空校验
                res_json["code"] = Enum.res_param_empty
                res_json["resMessage"] = "param empty"
            elif data.has_key("nickname") is False or data.has_key("sendcontent") is False: #参数缺失校验
                res_json["code"] = Enum.res_param_missing
                res_json["resMessage"] = "param missing"

            elif ic.send_message(chatroom_nickname=data["nickname"],content=data["sendcontent"]):
                res_json["code"] = Enum.res_success
                res_json["resMessage"] = "success"
            else:
                res_json["code"] = Enum.res_fail
                res_json["resMessage"] = "发送消息到群时发生异常，请联系15680502703"

    except Exception as result:
        res_json["code"] = Enum.res_fail
        res_json["resMessage"] = result
    finally:
        return jsonify(res_json)

@app.route('/api/uploadFile',methods = ['POST'])
def upload_file():      #上传单个文件
    res_json = {"resList": [], "code": "","resMessage": ""}  # 创建返回字典{"resList": [{"type": "noString", "id": 12}], "code": "1000", "resMessage": ""}
    resList_param = {}
    if request.method == 'POST':
        if 'file' not in request.files:
            res_json["code"] = Enum.res_param_is_not_file
            res_json["resMessage"] = "入参错误，不是文件类型"
        else:
            file = request.files['file']        #单个文件
            try:
                original_file_name = file.filename
                if allowed_upload_file_type(original_file_name) is False:
                    res_json["code"] = Enum.res_not_support_file_type
                    res_json["resMessage"] = "不支持该文件类型，支持的文件类型有：{0}".format(ALLOWED_UPLOAD_FILE_TYPE)
                else:
                    if os.path.exists(UPLOAD_FILE_PATH):
                        pass
                    else:
                        os.mkdir(UPLOAD_FILE_PATH)
                    t = time.time()
                    timestamp = int(round(t * 1000))
                    new_file_name =str(timestamp) + '.' + original_file_name.rsplit('.',1)[1]     #时间戳加后缀名，构成新文件名
                    file.save(os.path.join(UPLOAD_FILE_PATH,new_file_name))     #存储文件
                    resList_param["fileName"] = new_file_name
                    resList_param["originalFileName"] = original_file_name
                    resList_param["filePath"] = os.path.join(UPLOAD_FILE_PATH,new_file_name)
                    res_json["resList"].append(resList_param)
                    res_json["code"] = Enum.res_success
                    res_json["resMessage"] = "文件上传成功"
            except Exception as result:
                res_json["code"] = Enum.res_fail
                res_json["resMessage"] = "文件上传失败，请稍后重试，失败原因：{0}".format(result)
            finally:
                return jsonify(res_json)

@app.route('/api/uploadFiles',methods = ['POST'])
def upload_files():      #批量上传文件
    res_json = {"resList": [], "code": "","resMessage": ""}  # 创建返回字典{"resList": [{"type": "noString", "id": 12}], "code": "1000", "resMessage": ""}

    if request.method == 'POST':
        if 'file' not in request.files:
            res_json["code"] = Enum.res_param_is_not_file
            res_json["resMessage"] = "入参错误，不是文件类型"
        else:
            files = request.files.getlist('file')       #post参数中获取文件参数列表
            try:
                # resList_param = {'fileName': '', 'originalFileName': '', 'resState': False, 'resDescription': ''}     #初始化放这里 append会覆盖之前的值
                for file in files:
                    resList_param = {'fileName': '', 'originalFileName': '', 'resState': False, 'resDescription': ''}       #初始化返回的列表
                    try:
                        # print file
                        original_file_name = file.filename
                        if allowed_upload_file_type(original_file_name) is False:
                            resList_param["resState"] = False
                            resList_param['resDescription'] = "不支持该文件类型，支持的文件类型有：{0}".format(ALLOWED_UPLOAD_FILE_TYPE)
                        else:
                            if os.path.exists(UPLOAD_FILE_PATH):
                                pass
                            else:
                                os.mkdir(UPLOAD_FILE_PATH)
                            t = time.time()
                            timestamp = int(round(t * 1000))
                            new_file_name =str(timestamp) + '.' + original_file_name.rsplit('.',1)[1]     #时间戳加后缀名，构成新文件名
                            file.save(os.path.join(UPLOAD_FILE_PATH,new_file_name))     #存储文件
                            resList_param["fileName"] = new_file_name
                            resList_param["filePath"] = os.path.join(UPLOAD_FILE_PATH,new_file_name)
                            resList_param["resState"] = True
                            resList_param['resDescription'] = '成功'
                    except Exception as res:
                        resList_param["resState"] = False
                        resList_param['resDescription'] = "上传失败，原因：{0}".format(res)
                    finally:
                        resList_param["originalFileName"] = original_file_name
                        res_json["resList"].append(resList_param)
                        # print(id(res_json["resList"]["fileName"]))
                res_json["code"] = Enum.res_success
                res_json["resMessage"] = "文件上传成功"
            except Exception as result:
                res_json["code"] = Enum.res_fail
                res_json["resMessage"] = "文件上传失败，请稍后重试，失败原因：{0}".format(result)
            finally:
                return jsonify(res_json)

@app.route('/api/sendFilesToFriendOrChatroom',methods = ['POST'])
def send_file():        #发送文件给好友或者微信群
    try:
        res_json = {"resList": [], "code": "", "resMessage": ""}   #创建返回字典{"resList": [{"type": "noString", "id": 12}], "code": "1000", "resMessage": ""}
        if request.method == "POST":
            # print request.form.get('body')
            data = json.loads(request.get_data())   #将接口数据转为json
            if len(data) == 0 or data is None:  #参数为空校验
                res_json["code"] = Enum.res_param_empty
                res_json["resMessage"] = "param empty"
            elif data.has_key("fileName") is False or data.has_key("friendNickName") is False or data.has_key("chatroomNickName") is False: #参数缺失校验
                res_json["code"] = Enum.res_param_missing
                res_json["resMessage"] = "param missing"
            elif len(data['fileName']) == 0:
                res_json["code"] = Enum.res_param_empty
                res_json["resMessage"] = "文件名称为空"
            elif len(data["friendNickName"]) != 0:      #发送文件给好友
                res_json["code"] = Enum.res_success
                res_json["resMessage"] = "发送文件成功"
                for file_name in data["fileName"]:
                    file_path = UPLOAD_FILE_PATH + '\\'+ file_name
                    sub_dic = {}
                    # print type(data["friendNickName"])
                    if ic.send_file(file_path=file_path,friend_nickname=data["friendNickName"]):
                        sub_dic["resState"] = True
                        sub_dic["fileName"] = file_name
                    else:
                        sub_dic["resState"] = False
                        sub_dic["fileName"] = file_name
                        res_json["code"] = Enum.res_part_success
                        res_json["resMessage"] = "发送文件，部分成功，部分失败"
                    res_json["resList"].append(sub_dic)
            elif len(data["chatroomNickName"]) != 0:       #发送文件到群
                res_json["code"] = Enum.res_success
                res_json["resMessage"] = "发送文件成功"
                i = 0       #判断是否全部发送成功   如果i的计数小于data["fileName"]的长度，说明有发送失败
                for file_name in data["fileName"]:
                    file_path = UPLOAD_FILE_PATH + '\\'+ file_name
                    sub_dic = {}
                    if os.path.exists(file_path) is False:
                        sub_dic["resState"] = False
                        sub_dic["fileName"] = file_name
                    elif ic.send_file(file_path=file_path,chatroom_nickname=data["chatroomNickName"]):
                        sub_dic["resState"] = True
                        sub_dic["fileName"] = file_name
                        i = i + 1
                    else:
                        sub_dic["resState"] = False
                        sub_dic["fileName"] = file_name
                    res_json["resList"].append(sub_dic)
                if i == 0:
                    res_json["code"] = Enum.res_fail
                    res_json["resMessage"] = "发送文件失败"
                if len(data["fileName"]) != i and i != 0:
                    res_json["code"] = Enum.res_part_success
                    res_json["resMessage"] = "发送文件，部分成功，部分失败"
            else:
                res_json["code"] = Enum.res_fail
                res_json["resMessage"] = "发送文件失败"
                for file_name in data["fileName"]:
                    sub_dic = {}
                    sub_dic["resState"] = False
                    sub_dic["fileName"] = file_name
                    res_json["resList"].append(sub_dic)
    except Exception as result:
        res_json["code"] = Enum.res_fail
        res_json["resMessage"] = result
    finally:
        return jsonify(res_json)

@app.route('/api/sendTextOrFileToFriendOrChatroom',methods = ['POST'])
def send_content_file_friend_chatroom():
    res_json = {"sendFriendContent":[],"sendChatroomContent":[],"sendFriendFiles":[],"sendChatroomFiles":[]}
    if request.method == "POST":
        data = json.loads(request.get_data())
        if data.has_key("content") and len(data["content"]) != 0:
            if len(data["content"][0]["content"]) != 0:
                if data["content"][0]["sendFriend"] is True:        #发送文本给好友
                    for nick_name in data["friendNickName"]:
                        resList = {}
                        if ic.send_message(friend_nickname=nick_name,content=data["content"][0]["content"]):
                            resList["resStatus"] = True
                            resList["nickName"] = nick_name
                        else:
                            resList["resStatus"] = False
                            resList["nickName"] = nick_name
                        res_json["sendFriendContent"].append(resList)

                if data["content"][0]["sendChatroom"] is True:      #发送文本到群
                    for chatroom_nickname in data["chatroomNickName"]:
                        resList = {}
                        if ic.send_message(chatroom_nickname=chatroom_nickname,content=data["content"][0]["content"]):
                            resList["resStatus"] = True
                            resList["nickName"] = chatroom_nickname
                        else:
                            resList["resStatus"] = False
                            resList["nickName"] = chatroom_nickname
                        res_json["sendChatroomContent"].append(resList)

        if data.has_key("files") and len(data["files"]) != 0:
            if len(data["files"][0]["fileNames"]) != 0:
                if data["files"][0]["sendFriend"] is True:      #发送文件给好友
                    for file in data["files"][0]["fileNames"]:
                        file_path = UPLOAD_FILE_PATH + '\\'+ file
                        for nick_name in data["friendNickName"]:
                            resList = {}
                            if os.path.exists(file_path) is False:
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = False
                                resList["nickName"] = ''
                                resList["resDescribe"] = "文件不存在"
                                res_json["sendFriendFiles"].append(resList)
                                break
                            if ic.send_file(friend_nickname=nick_name,file_path=file_path):
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = True
                                resList["nickName"] = nick_name
                                resList["resDescribe"] = "成功"
                            else:
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = False
                                resList["nickName"] = nick_name
                                resList["resDescribe"] = "失败"
                            res_json["sendFriendFiles"].append(resList)

                if data["files"][0]["sendChatroom"] is True:      #发送文件到群
                    for file in data["files"][0]["fileNames"]:
                        file_path = UPLOAD_FILE_PATH + "\\" + file
                        for chatroom_nickname in data["chatroomNickName"]:
                            resList = {}
                            if os.path.exists(file_path) is False:
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = False
                                resList["chatrootNickName"] = ''
                                resList["resDescribe"] = "文件不存在"
                                res_json["sendChatroomFiles"].append(resList)
                                break
                            if ic.send_file(chatroom_nickname=chatroom_nickname, file_path=file_path):
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = True
                                resList["chatrootNickName"] = chatroom_nickname
                                resList["resDescribe"] = "成功"
                            else:
                                resList["fileName"] = file
                                resList["filePath"] = file_path
                                resList["resStatus"] = False
                                resList["chatrootNickName"] = chatroom_nickname
                                resList["resDescribe"] = "失败"
                            res_json["sendChatroomFiles"].append(resList)
    scc = 0
    if len(res_json["sendChatroomContent"]) != 0:
        for list in res_json["sendChatroomContent"]:
            if list["resStatus"] is True:
                scc = scc + 1
    if scc == 0 or len(res_json["sendChatroomContent"]) == scc:
        scf = 0
        if len(res_json["sendChatroomFiles"]) != 0:
            for list in res_json["sendChatroomFiles"]:
                if list["resStatus"] is True:
                    scf = scf +1
        if scf == 0 or len(res_json["sendChatroomFiles"]) == scf:
            sfc = 0
            if len(res_json["sendFriendContent"]) != 0:
                for list in res_json["sendFriendContent"]:
                    if list["resStatus"] is True:
                        sfc = sfc + 1
            if sfc == 0 or len(res_json["sendFriendContent"]) == sfc:
                sff = 0
                if len(res_json["sendFriendFiles"]) != 0:
                    for list in res_json["sendFriendFiles"]:
                        if list["resStatus"] is True:
                            sff = sff + 1
                if sff == 0 and sfc == 0 and scf == 0 and sff == 0:
                    res_json["code"] = Enum.res_fail
                    res_json["resMessage"] = "失败"
                    return jsonify(res_json)
                elif sff == len(res_json["sendFriendContent"]) and sfc == len(res_json["sendFriendContent"]) and scf == len(res_json["sendChatroomFiles"]) and sff == len(res_json["sendFriendFiles"]):
                    res_json["code"] = Enum.res_success
                    res_json["resMessage"] = "成功"
                    return jsonify(res_json)
                else:
                    res_json["code"] = Enum.res_part_success
                    res_json["resMessage"] = "部分成功"
                    return jsonify(res_json)
            else:
                res_json["code"] = Enum.res_part_success
                res_json["resMessage"] = "部分成功"
                return jsonify(res_json)
        else:
            res_json["code"] = Enum.res_part_success
            res_json["resMessage"] = "部分成功"
            return jsonify(res_json)
    else:
        res_json["code"] = Enum.res_part_success
        res_json["resMessage"] = "部分成功"
        return jsonify(res_json)

def allowed_upload_file_type(file_name):        #校验允许上传的文件类型
    return file_name and file_name.rsplit('.',1)[1] in ALLOWED_UPLOAD_FILE_TYPE

if __name__ == '__main__':
    ic = Itchat()
    app.run(debug=True)