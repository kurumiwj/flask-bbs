from flask_mail import Message
from extensions import mail
from celery import Celery

#定义任务函数
def send_mail(recipient,subject,body):
    message=Message(subject=subject,recipients=[recipient],body=body)
    mail.send(message)
    print("发送成功！")

#创建Celery对象
def make_celery(app):
    celery=Celery(app.import_name,backend=app.config["CELERY_RESULT_BACKEND"],broker=app.config["CELERY_BROKER_URL"])
    task=celery.Task
    class ContextTask(task):
        abstract=True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return task.__call__(self,*args,**kwargs)
    celery.Task=ContextTask
    app.celery=celery
    #添加任务
    celery.task(name="send_mail")(send_mail)
    return celery