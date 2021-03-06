#-*-coding:utf-8-*-
import os
import sys
sys.path.append("..")

from env import android

from utils import Utils
import shutil
import platform

def get_source():
    downloadUrl =  'https://curl.haxx.se/download/curl-%s.zip'%('7.64.1',)
    
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


def addMbedtlSDependencies(cwd,platformName,build_type,abi):
    MBEDTLS_INCLUDE_DIRS = os.path.join(cwd,platformName,build_type, 'mbedtls', abi, "include" )
    MBEDTLS_LIBRARY = os.path.join(cwd,platformName,build_type, 'mbedtls', abi, "lib/libmbedtls.a" ) 
    MBEDX509_LIBRARY = os.path.join(cwd,platformName,build_type, 'mbedtls', abi, "lib/libmbedx509.a" ) 
    MBEDCRYPTO_LIBRARY  = os.path.join(cwd,platformName,build_type, 'mbedtls', abi, "lib/libmbedcrypto.a" ) 
    

    return " -DCMAKE_USE_OPENSSL=0  -DCMAKE_USE_MBEDTLS=1 -DMBEDTLS_INCLUDE_DIRS=%s -DMBEDTLS_LIBRARY=%s -DMBEDX509_LIBRARY=%s -DMBEDCRYPTO_LIBRARY=%s "% (
        MBEDTLS_INCLUDE_DIRS, MBEDTLS_LIBRARY,MBEDX509_LIBRARY,  MBEDCRYPTO_LIBRARY)

   


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
    cmake_arguments = addMbedtlSDependencies(cwd,platformName,build_type,abi)

    if platformName == "android":
        androidEnv = android.Android()
        CMAKE_BIN =  androidEnv.getCmakeBin()
        cmake_arguments = androidEnv.getCmakeArg(abi) + addMbedtlSDependencies(cwd,platformName,build_type,abi)


    cmd = '''%s %s -DCMAKE_INSTALL_PREFIX=%s \
        -DCMAKE_BUILD_TYPE=%s  \
        -DHAVE_POLL_FINE_EXITCODE=0 \
        -DBUILD_SHARED_LIBS=0 \
        -DCMAKE_USE_OPENSSL=0 ..'''%(CMAKE_BIN,cmake_arguments,installPath, build_type ) 
    
    Utils.runCmd(cmd)
    Utils.runCmd("%s --build ."%(CMAKE_BIN , ))
    os.system("%s -P cmake_install.cmake"%(CMAKE_BIN, ))

    os.chdir(cwd)


if __name__ == "__main__":
    abiList = ['armeabi-v7a', "arm64-v8a", "x86",'x86_64']
    for abi in abiList:
        do_build("android", abi = abi)
  