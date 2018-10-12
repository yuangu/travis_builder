#-*-coding:utf-8-*-

import os
from config  import config
import importlib
 

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

def doAfterBuild(env_config, install_path): 
    pass  

def doBuild(env_config, install_path = "."):
    build_script = env_config['build_script']
    
    for k in build_script.keys():
        build_config = build_script[k]
        if "needBuild" not in build_config.keys() or not build_config["needBuild"]:
            continue

        #加载构建器
        builder = importlib.import_module("Android." + k )
        builder.do_build(build_script[k], install_path)
        doAfterBuild(env_config, install_path)


def main():
    build_target = os.environ["BUILD_TARGET"]
    env_config = config[build_target]
    
    if not doBeforeBuild(env_config):
        return
    doBuild(env_config)
   
if __name__ == "__main__":
    main()


    


