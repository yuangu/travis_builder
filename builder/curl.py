#-*-coding:utf-8-*-
import os
import sys
sys.path.append("..")

from env import android

from utils import Utils
import shutil
import platform

def get_source():
    downloadUrl =  'https://curl.haxx.se/download/curl-%s.zip'%('7.61.1',)
    
    outZipPath = os.path.join("./", os.path.basename(downloadUrl))
    if not os.path.isfile(outZipPath):
        Utils.download(downloadUrl,   outZipPath)
    
    Utils.extractZipFile(outZipPath)
    
    (filepath,tempfilename) = os.path.split(outZipPath)
    (shotname,extension) = os.path.splitext(tempfilename)
    #获取源代码
    cwd = os.getcwd()
    srcPath = os.path.join(cwd, shotname)

    return srcPath
    

def do_build(platformName = platform.system().lower(), build_type = "Release", abi = "armeabi-v7a"):
    #获取源代码
    cwd = os.getcwd()

    installPath = os.path.join(cwd,platformName,build_type,abi)
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
        cmake_arguments = androidEnv.getCmakeArg(build_type, abi)


    cmd = '''%s %s -DCMAKE_INSTALL_PREFIX=%s \
        -DCMAKE_BUILD_TYPE=%s  \
        -DHAVE_POLL_FINE_EXITCODE=0 \
        -DCMAKE_USE_OPENSSL=0 ..'''%(CMAKE_BIN,cmake_arguments,installPath, build_type ) 
    
    Utils.runCmd(cmd)
    Utils.runCmd("%s --build ."%(CMAKE_BIN , ))
    os.system("%s -P cmake_install.cmake"%(CMAKE_BIN, ))

    os.chdir(cwd)


if __name__ == "__main__":
    do_build(abi="")
  