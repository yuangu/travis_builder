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
    

def do_build():
    #获取源代码
    cwd = os.getcwd()
    build_type = "Release"
    abi = "armeabi-v7a"
    installPath = os.path.join(cwd ,build_type,abi)
    srcPath = get_source()
    os.chdir(srcPath)

    buildDir = os.path.join(srcPath, "build")
    Utils().cleanFile(buildDir)
    Utils().mkDir(buildDir)
    os.chdir(buildDir)

    androidEnv = android.Android()
    ANDROID_CMAKE =  androidEnv.getCmakeBin()
    cmake_arguments = androidEnv.getCmakeArg()


    cmd = '''%s %s -DCMAKE_INSTALL_PREFIX=%s -DHAVE_POLL_FINE_EXITCODE=0 -DCMAKE_USE_OPENSSL=0 ..'''%(ANDROID_CMAKE,cmake_arguments,installPath ) 
    
    Utils.runCmd(cmd)
    Utils.runCmd("%s --build ."%(ANDROID_CMAKE, ))
    os.system("%s -P cmake_install.cmake"%(ANDROID_CMAKE, ))

    os.chdir(cwd)


if __name__ == "__main__":
    do_build()
  