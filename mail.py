#-*-coding:utf-8-*-
import os

from email import MIMEMultipart
from email import MIMEText
from email import MIMEBase
from email import Encoders 
from email.Utils import formatdate
import smtplib

def sendmail(smtpServer, username, passwd, toMail, subject, msg, file_name):    
    server = smtplib.SMTP('smtp.126.com')
    server.login(username,passwd)
    main_msg = MIMEMultipart.MIMEMultipart()
    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = MIMEText.MIMEText( msg,'plain', "utf-8")
    main_msg.attach(text_msg)
    
    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)
    
    ## 读入文件内容并格式化
    data = open(file_name, 'rb')
    file_msg = MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read( ))
    data.close( )
    Encoders.encode_base64(file_msg)
    
    ## 设置附件头
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition',
    'attachment', filename = basename)
    main_msg.attach(file_msg)
    
    # 设置根容器属性
    main_msg['From'] = username
    main_msg['To'] = "1143402671@qq.com"
    # main_msg['Subject'] = "[sxtwl]打包结果通知"
    main_msg['Date'] = formatdate( )
    
    #带上python版本的信息   
    main_msg['Subject'] = subject

    # 得到格式化后的完整文本
    fullText = main_msg.as_string( )
    
    # 用smtp发送邮件
    try:
        server.sendmail(main_msg['From'], main_msg['To'], fullText)
    finally:
        server.quit()

if __name__ == "__main__":
    #帐号和密码来源https://github.com/normal-four/test/blob/815393a266142ba64df0402f9a6c15c203b95156/spider/mailtest.py
    username = "wzp_test@126.com"
    passwd = "a1269325139"
    subject = u"测试邮件"
    msg = u"这是一封测试邮件" 
    file_name = "./config.py"
    sendmail('smtp.126.com',username, passwd, "1143402671@qq.com",subject, msg ,file_name)