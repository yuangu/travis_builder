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

    downloadUrl =  'https://tls.mbed.org/download/mbedtls-%s-apache.tgz'%(config['version'],)
    
    outZipPath = os.path.join("./", os.path.basename(downloadUrl))
   

    if not os.path.isfile(outZipPath):
        Utils.download(downloadUrl,   outZipPath)
    
    Utils.cleanFile("./mbedtls")
    Utils.mkDir("./mbedtls")
    Utils.extractTarFile(outZipPath, "./mbedtls")
   
    #解压完毕,进入源代码目录
    mbedtls_dir_list = os.listdir('./mbedtls')

    #获取源代码
    cwd = os.getcwd()
    srcPath = os.path.join(cwd, mbedtls_dir_list[0])
    os.chdir(srcPath)

    ANDROID_SDK = Utils.getOSEnviron("ANDROID_SDK_ROOT")
    ANDROID_NDK = Utils.getOSEnviron("ANDROID_NDK_ROOT")
    CMAKE_DIR = getCmakeDir(ANDROID_SDK)


    ANDROID_CMAKE = os.path.join(CMAKE_DIR, 'bin/cmake')
    ANDROID_NINJA=os.path.join(CMAKE_DIR,'bin/ninja')
    

    Utils().cleanFile(installPath)
    
    buildDir = os.path.join(srcPath, "build")

    cmake_arguments= ""
    if 'cmake_arguments' in config.keys():
        cmake_arguments= config['cmake_arguments']

    android_api_level = "android-16"
    if "android_api" in config.keys():
        android_api_level = config["android_api"]


    build_type_list = ["Release"]
    if 'build_type' in config.keys():
        build_type_list = config['build_type']

    for build_type in  build_type_list:
        for abi in abiList:
            os.chdir(srcPath)
            Utils().cleanFile(buildDir)
            Utils().mkDir(buildDir)
            os.chdir(buildDir)
            
            cmd = '''%s -DANDROID_ABI=%s   \
            -DANDROID_PLATFORM=%s  \
            -DCMAKE_BUILD_TYPE=%s  \
            -DANDROID_NDK=%s    \
            -DCMAKE_CXX_FLAGS=-std=c++11 -frtti -fexceptions   \
            -DCMAKE_TOOLCHAIN_FILE=%s/build/cmake/android.toolchain.cmake    \
            -DCMAKE_MAKE_PROGRAM=%s -G "Ninja"    \
            -DENABLE_TESTING=0    \
            %s \
            -DCMAKE_INSTALL_PREFIX=%s \
            ..'''%(ANDROID_CMAKE,abi,android_api_level,build_type,ANDROID_NDK,ANDROID_NDK,ANDROID_NINJA, cmake_arguments,  os.path.join(installPath,build_type,abi) ) 
            
            Utils.runCmd(cmd)
            Utils.runCmd("%s --build ."%(ANDROID_CMAKE, ))
            os.system("%s -P cmake_install.cmake"%(ANDROID_CMAKE, ))

    os.chdir(cwd)