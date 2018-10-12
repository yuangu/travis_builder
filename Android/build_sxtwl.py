#-*-coding:utf-8-*-
import os

def do_build(config, installPath):
    cmd_lists = (
        "git clone https://github.com/yuangu/sxtwl_cpp.git",
        "cd sxtwl_cpp && python ndk_build.py"
    )

    for cmd in cmd_lists:
        os.system(cmd)


