#-*-coding:utf-8-*-

import os
from config  import config
import importlib

#获取python文件所在的路径
def p():
    frozen = "not"
    if getattr(sys, 'frozen',False):
        frozen = "ever so"
        return os.path.dirname(sys.executable)

    return os.path.split(os.path.realpath(__file__))[0]

import sys 
sys.path.append(p()) 

def main():
    build_target = os.environ["BUILD_TARGET"]
    env_config = config[build_target]
    
    if build_target  == 'Android':
        #配置系统环境
        from android_env import config_env
        config_env(env_config)
        
        #正式构建
        for v in env_config['build_script']:
            build_script = importlib.import_module("Android." + v)
            build_script.do_build()

if __name__ == "__main__":
    main()


    


