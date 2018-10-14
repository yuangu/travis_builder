#-*-coding:utf-8-*-
import os
from utils import Utils
import shutil
import platform

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
    #需要打包的abi
    abiList = [ ]
    if config != None and "abiList" in config.keys():
        abiList.extend(config["abiList"])
    if len(abiList) <= 0:
        return
    
    #获取源代码
    cwd = os.getcwd()
    srcPath = os.path.join(cwd, "sxtwl_cpp")
    if os.path.isdir(srcPath):
        os.chdir(srcPath)
        os.system("git pull")
        os.chdir(cwd)
    else:
        os.system( "git clone https://github.com/yuangu/sxtwl_cpp.git")

    ANDROID_SDK = Utils.getOSEnviron("ANDROID_SDK_ROOT")
    ANDROID_NDK = Utils.getOSEnviron("ANDROID_NDK_ROOT")
    CMAKE_DIR = getCmakeDir(ANDROID_SDK)


    ANDROID_CMAKE = os.path.join(CMAKE_DIR, 'bin/cmake')
    ANDROID_NINJA=os.path.join(CMAKE_DIR,'bin/ninja')
  
    Utils().cleanFile(installPath)
    
    android_api_level = "android-16"
    if "android_api" in config.keys():
        android_api_level = config["android_api"]

    buildDir = os.path.join(srcPath, "build")

    build_type_list = ["Release"]
    if 'build_type' in config.keys():
        build_type_list = config['build_type']

    for build_type in  build_type_list:
        for abi in abiList:
            for abi in abiList:
                os.chdir(srcPath)
                Utils().cleanFile(buildDir)
                Utils().mkDir(buildDir)
                os.chdir(buildDir)
                
                cmd = '''%s -DANDROID_ABI=%s   \
                -DANDROID_PLATFORM=%s  \
                -DCMAKE_BUILD_TYPE=%s   \
                -DANDROID_NDK=%s    \
                -DCMAKE_CXX_FLAGS=-std=c++11 -frtti -fexceptions   \
                -DCMAKE_TOOLCHAIN_FILE=%s/build/cmake/android.toolchain.cmake    \
                -DCMAKE_MAKE_PROGRAM=%s -G "Ninja"    \
                -DCONSOLE=1   \
                -DSXTWL_WRAPPER_JAVA=1  \
                -DCMAKE_INSTALL_PREFIX=%s \
                ..'''%(ANDROID_CMAKE,abi,android_api_level,build_type,ANDROID_NDK,ANDROID_NDK,ANDROID_NINJA, installPath ) 
                

                Utils.runCmd(cmd)
                Utils.runCmd("%s --build ."%(ANDROID_CMAKE, ))
                
                #不存在导出的java文件，则导出
                outJavaPath = os.path.join(installPath, build_type, "java/com/huoyaojing")
                if not os.path.isdir(outJavaPath):
                    Utils().mkDir(outJavaPath)
                    fileList = Utils.getAllDirFiles(buildDir, [".java"])
                    for tmp in fileList:
                        basename =  os.path.basename(tmp)
                        shutil.move(tmp, os.path.join(outJavaPath, basename))

                #打包so库
                outSoPath = os.path.join(installPath, build_type, "jniLibs/" + abi)
                Utils().cleanFile(outSoPath)
                Utils().mkDir(outSoPath)
                fileList = Utils.getAllDirFiles(buildDir, [".so"])
                for tmp in fileList:
                    basename =  os.path.basename(tmp)
                    shutil.move(tmp, os.path.join(outSoPath, "libsxtwl_java.so"))
    
    #还原目录
    os.chdir(cwd)


