#-*-coding:utf-8-*-

import os
from config  import config
import importlib
from utils import Utils
from mail import sendmail
import sys

def doBeforeBuild(env_config):    
    #判断是否有构建项
    build_script = env_config['build_script']
    hasNeedBuildPackage = False 
    for k in build_script.keys():
        build_config = build_script[k]
        if "needBuild" in build_config.keys() and build_config["needBuild"]:
            hasNeedBuildPackage = True
            break
    if not hasNeedBuildPackage:
        return False
    
    #配置环境 
    from android_env import do_config
    do_config(env_config)
    return True

def doAfterBuild(build_config, install_path):
    name = build_config["name"]
    file_name = "./pack.zip"
    Utils.cleanFile(file_name)
    Utils.makeZipFile(file_name, install_path)

    subject = u"自动打包 %s (%s)"%(name,  os.environ["BUILD_TARGET"])
    msg = u"这是一封自动发送的邮件，请不回复" 
    mail_config = config['mail']

    try_time = 0
    while(try_time < 3):
        try:
            try_time = try_time + 1
            print "try sendmail @ time:" + str(try_time)
            sendmail(mail_config['smtp_server'] ,mail_config['smtp_username'], mail_config['smtp_passwd'], mail_config['to_mail'],subject, msg ,file_name)
            break
        except:
            pass

def doBuild(env_config):
    build_script = env_config['build_script']
    
    for k in build_script.keys():
        build_config = build_script[k]
        if "needBuild" not in build_config.keys() or not build_config["needBuild"]:
            continue

        #加载构建器
        name = build_config["name"]
        install_path = os.path.join("./build_out", name)
        install_path = os.path.abspath(install_path)
        Utils.cleanFile(install_path)
        builder = importlib.import_module("Android." + k )
        builder.do_build(build_script[k], install_path)
        doAfterBuild(build_script[k], install_path)

def main(build_target):    
    env_config = config[build_target]
    
    if not doBeforeBuild(env_config):
        return
    doBuild(env_config)
   
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print "python main.py build_platform_name"


    


