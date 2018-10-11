#-*-coding:utf-8-*-

import os
from config  import config

import importlib

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


    


