#-*-coding:utf-8-*-

from Android  import build_sxtwl
import os
from utils import Utils
from mail import sendmail
from config  import config
os.environ["BUILD_TARGET"] = "Android"
if __name__ == "__main__":
    # build_sxtwl.do_build("", os.path.abspath("./out"))
    

    name = "test_sxtwl"
    file_name = "./pack.zip"
    Utils.makeZipFile(file_name, os.path.abspath("./out"))

    subject = u"自动打包 %s (%s)"%(name,  os.environ["BUILD_TARGET"])
    msg = u"这是一封自动发送的邮件，请不回复" 
    mail_config = config['mail']
    sendmail(mail_config['smtp_server'] ,mail_config['smtp_username'], mail_config['smtp_passwd'], mail_config['to_mail'],subject, msg ,file_name)