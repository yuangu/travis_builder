#-*-coding:utf-8-*-
import os
from utils import Utils

def getCmakeDir(ANDROID_SDK):
    ndk_cmake_dir  = os.path.join(ANDROID_SDK,  "cmake")
    if  not  os.path.isdir(ndk_cmake_dir):
        return None
    
    cmake_dir_list = os.listdir(ndk_cmake_dir)
    list_len = len(cmake_dir_list)
    if list_len <= 0:
        return  None
    
    return os.path.join(ndk_cmake_dir, cmake_dir_list[list_len - 1] )


def do_build(config, installPath):
    cmd_lists = (
        "git clone https://github.com/yuangu/sxtwl_cpp.git",
        #"cd sxtwl_cpp && python ndk_build.py"
    )

    for cmd in cmd_lists:
        os.system(cmd)

    ANDROID_SDK = Utils.getOSEnviron("ANDROID_SDK_ROOT")
    ANDROID_NDK = Utils.getOSEnviron("ANDROID_NDK_ROOT")
    CMAKE_DIR = getCmakeDir(ANDROID_SDK)


    ANDROID_CMAKE = os.path.join(CMAKE_DIR, 'bin/cmake')
    ANDROID_NINJA=os.path.join(CMAKE_DIR,'bin/ninja')

    Utils().cleanFile(installPath)
    
    #需要打包的abi
    abiList = [
        'armeabi',
        'armeabi-v7a',
        "arm64-v8a",
        "x86",
        'x86_64',
        'mips',
        'mips64',
    ]

    cwd = os.getcwd()
    pyPath = os.path.join(cwd, "sxtwl_cpp")
    buildDir = os.path.join(pyPath, "build")
    for abi in abiList:
        os.chdir(pyPath)
        Utils().cleanFile(buildDir)
        Utils().mkDir(buildDir)
        os.chdir(buildDir)
        
        cmd = '''%s -DANDROID_ABI=%s   \
        -DANDROID_PLATFORM=android-16  \
        -DCMAKE_BUILD_TYPE=Release   \
        -DANDROID_NDK=%s    \
        -DCMAKE_CXX_FLAGS=-std=c++11 -frtti -fexceptions   \
        -DCMAKE_TOOLCHAIN_FILE=%s/build/cmake/android.toolchain.cmake    \
        -DCMAKE_MAKE_PROGRAM=%s -G "Ninja"    \
        -DCONSOLE=1   \
        -DSXTWL_WRAPPER_JAVA=1  \
        -DCMAKE_INSTALL_PREFIX=%s \
        ..'''%(ANDROID_CMAKE,abi,ANDROID_NDK,ANDROID_NDK,ANDROID_NINJA, installPath ) 
        
        Utils.runCmd(cmd)
        Utils.runCmd("%s --build ."%(ANDROID_CMAKE, ))
        Utils.runCmd("%s -P cmake_install.cmake"%(ANDROID_CMAKE, ))
    
    #还原目录
    os.chdir(cwd)