#-*-coding:utf-8-*-
import os

def do_build():
    cmd = (
        "git clone https://github.com/yuangu/sxtwl_cpp.git"
        "cd sxtwl_cpp && python ndk_build.py"
    )

    os.system(cmd)


