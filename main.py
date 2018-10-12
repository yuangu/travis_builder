#-*-coding:utf-8-*-

import os
from config  import config
import sys
import traceback
 
 
def import_class(import_str):
    """Returns a class from a string including module and class.
    .. versionadded:: 0.3
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))
 
 
def import_object(import_str, *args, **kwargs):
    """Import a class and return an instance of it.
    .. versionadded:: 0.3
    """
    return import_class(import_str)(*args, **kwargs)
 
 
def import_module(import_str):
    """Import a module.
    .. versionadded:: 0.3
    """
    print import_str
    __import__(import_str)
    return sys.modules[import_str]

#获取python文件所在的路径
def p():
    frozen = "not"
    if getattr(sys, 'frozen',False):
        frozen = "ever so"
        return os.path.dirname(sys.executable)

    return os.path.split(os.path.realpath(__file__))[0]

import sys 
sys.path.append(p()) 

build_script = import_module("Android." + "build_sxtwl")

def main():
    build_target = os.environ["BUILD_TARGET"]
    env_config = config[build_target]
    
    if build_target  == 'Android':
        #配置系统环境
        from android_env import config_env
        config_env(env_config)
        
        #正式构建
        for v in env_config['build_script']:
            build_script = import_module("Android." + v)
            build_script.do_build()

if __name__ == "__main__":
    main()


    


