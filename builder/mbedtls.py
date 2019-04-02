#-*-coding:utf-8-*-
import os
import sys
sys.path.append("..")

from env import android

from utils import Utils
import shutil
import platform

def get_source():
    downloadUrl =  'https://tls.mbed.org/download/mbedtls-%s-apache.tgz'%('2.16.1',)
    
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
    srcPath = os.path.join(cwd,'./mbedtls', mbedtls_dir_list[0])
    
    return srcPath


def do_build(platformName = platform.system().lower(), build_type = "Release", abi = "armeabi-v7a"):
    #获取源代码
    cwd = os.getcwd()
    libName = os.path.splitext(os.path.basename(os.path.basename(__file__)))[0]
    installPath = os.path.join(cwd,platformName,build_type,libName,abi)
    srcPath = get_source()
    os.chdir(srcPath)

    buildDir = os.path.join(srcPath, "build")
    Utils().cleanFile(buildDir)
    Utils().mkDir(buildDir)
    os.chdir(buildDir)

    CMAKE_BIN =  "cmake "
    cmake_arguments = ""

    if platformName == "android":
        androidEnv = android.Android()
        CMAKE_BIN =  androidEnv.getCmakeBin()
        cmake_arguments = androidEnv.getCmakeArg(abi)


    cmd = '''%s %s -DCMAKE_INSTALL_PREFIX=%s \
        -DCMAKE_BUILD_TYPE=%s  \
        -DENABLE_PROGRAMS=0 \
        -DENABLE_TESTING=0 \
        -DCMAKE_USE_OPENSSL=0 ..'''%(CMAKE_BIN,cmake_arguments,installPath, build_type ) 
    
    Utils.runCmd(cmd)
    Utils.runCmd("%s --build ."%(CMAKE_BIN , ))
    os.system("%s -P cmake_install.cmake"%(CMAKE_BIN, ))

    os.chdir(cwd)


if __name__ == "__main__":
    abiList = ['armeabi-v7a', "arm64-v8a", "x86",'x86_64']
    for abi in abiList:
        do_build("android", abi = abi)