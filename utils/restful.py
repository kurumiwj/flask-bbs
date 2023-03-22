from flask import jsonify

class HttpCode(object):
    #响应正常
    ok=200
    #未授权
    unAuthorizedError=401
    #没有权限
    permissionError=403
    #客户端参数错误
    paramsError=400
    #服务器错误
    serverError=500

def restful_result(code,message,data):
    return jsonify({"code":code,"msg":message or "","data":data or {}}),code

def ok(message=None,data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)

def un_authorized_error(message="用户未登录！"):
    return restful_result(code=HttpCode.unAuthorizedError,message=message,data=None)

def permission_error(message="没有权限访问！"):
    return restful_result(code=HttpCode.permissionError,message=message,data=None)

def params_error(message="参数错误！"):
    return restful_result(code=HttpCode.paramsError,message=message,data=None)

def server_error(message="服务器开小差啦！"):
    return restful_result(code=HttpCode.serverError,message=message,data=None)