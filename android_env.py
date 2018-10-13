#-*-coding:utf-8-*-

import os
from utils import Utils
import platform


def hasCmake(ANDROID_SDK):
    ndk_cmake_dir  = os.path.join(ANDROID_SDK,  "cmake")
    if  not  os.path.isdir(ndk_cmake_dir):
        return False
    
    cmake_dir_list = os.listdir(ndk_cmake_dir)
    list_len = len(cmake_dir_list)
    if list_len <= 0:
        return  False
    
    for v in cmake_dir_list:
        cmake_bin = os.path.join(ndk_cmake_dir, v, 'source.properties')     
        if os.path.isfile(cmake_bin):
            return True
    
    return False

def hasNDK(ANDROID_SDK):
    ndk_properties = os.path.join(ANDROID_SDK, "ndk-bundle/source.properties")
    if os.path.exists(ndk_properties ):
        return True
    return False

def getPackageVersion(packPath):
    with open(os.path.join(packPath, "source.properties")) as f:
        for  line in  f.readlines(): 
            v = line.split('=')
            if len(v) != 2:
                continue
            key = v[0].strip()  
            if key == "Pkg.Revision":
                value = v[1].strip()                
                return value
    
    return None



def do_config(config):
    #更新NDK配置NDK
    if Utils.getOSEnviron("ANDROID_NDK_ROOT") == None and  "ndk" in config and config["ndk"] !=  None:
        ndk_url =  config["ndk"] 

        #判断本地的ndk
        needDownload  = True
        android_sdk_zip = "android_ndk.zip"    
        if os.path.isfile(android_sdk_zip) and ("ndk_sha_1" in config) and config["ndk_sha_1"] != None:
            sha1 = Utils.sha1_checksum(android_sdk_zip)         
            if sha1.lower() == config["ndk_sha_1"]:
                print "exist android_ndk.zip"
                needDownload =  False

        #需要下载NDK
        if needDownload:
            Utils.download(ndk_url, android_sdk_zip)
        
        #解压NDK
        Utils.cleanFile("./android_ndk")
        Utils.extractZipFile(android_sdk_zip,  "./android_ndk")
        
        #获取NDK真实的地址
        extractZipFilePath = os.path.realpath("./android_ndk")
        extractZipFilePath_dir_list = os.listdir(extractZipFilePath)
        list_len = len(extractZipFilePath_dir_list)
        if list_len <= 0:
            return  False
       
        NDK_ROOT = os.path.join(extractZipFilePath, extractZipFilePath_dir_list[list_len - 1] )
        
        #在linux机器上可能会有权限问题
        if "windows" != platform.system().lower():
            Utils.runCmd("chmod -R 775 %s"%(NDK_ROOT,))

        Utils.setOSEnviron("ANDROID_NDK_ROOT", NDK_ROOT) 

    #更新android sdk
    if Utils.getOSEnviron("ANDROID_SDK_ROOT") != None:
        components = []

        if "components" in config and len(config["components"]) > 0:
            components.extend(config["components"])
            
        #检查是否存在ndk的配置
        if  Utils.getOSEnviron("ANDROID_NDK_ROOT") == None:
            Utils.setOSEnviron("ANDROID_NDK_ROOT", os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "ndk-bundle"))
            if not hasNDK(Utils.getOSEnviron("ANDROID_SDK_ROOT")) and "ndk-bundle" not in components:
                components.append("ndk-bundle")
                       
        #检查cmake的配置
        if not hasCmake(Utils.getOSEnviron("ANDROID_SDK_ROOT")):
            components.append("cmake;3.6.4111459")

        #update android sdk
        if  len(components) > 0:
            Utils.setOSEnviron("TERM", "dumb")        
            with open( os.path.join(os.environ['HOME'],  '.android/repositories.cfg'), "w+" ) as f:
                pass

            android_sdk_licenses_dirs = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "licenses")
            Utils.mkDir( android_sdk_licenses_dirs )
            
            with open( os.path.join(android_sdk_licenses_dirs, 'android-sdk-license'), "w+" ) as f:
                f.write("\n8933bad161af4178b1185d1a37fbf41ea5269c55")
                f.write("\nd56f5187479451eabf01fb78af6dfcb131a6481e")

            sdkmanager = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"),  "tools/bin/sdkmanager")
            if "windows" == platform.system().lower():
                Utils.runCmd('%s --update > NUL' % (sdkmanager, ) )
            else:
                Utils.runCmd('%s --update > /dev/null' % (sdkmanager, ) )

            componentsStr = " ".join( '"%s"'%(v, ) for v in components)
            if "windows" == platform.system().lower():
                cmd = 'echo y | %s   %s > NUL' % (sdkmanager,  componentsStr)
                Utils.runCmd(cmd)
            else:
                cmd = 'echo "y" | %s   %s > /dev/null' % (sdkmanager,  componentsStr)
                Utils.runCmd(cmd)

    #打印ndk版本
    NDK_ROOT = Utils.getOSEnviron("ANDROID_NDK_ROOT")
    if NDK_ROOT != None:
        print "NDK Version:%s" %(getPackageVersion(NDK_ROOT),)

if __name__ == "__main__":
    config = {
        "ndk": 'https://dl.google.com/android/repository/android-ndk-r16b-linux-x86_64.zip',    #ndk下载地址
        "ndk_sha_1":'42aa43aae89a50d1c66c3f9fdecd676936da6128',
    }

    do_config(config)