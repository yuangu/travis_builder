#-*-coding:utf-8-*-

import os
from utils import Utils

def do_config(config):
    Utils.setOSEnviron("TERM", "dumb")
    Utils.setOSEnviron("ANDROID_SDK_ROOT", "/usr/local/android-sdk")

    Utils.runCmd("touch ~/.android/repositories.cfg")
    android_sdk_licenses_dirs = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "licenses")
    Utils.mkDir( android_sdk_licenses_dirs )
    
    with open( os.path.join(android_sdk_licenses_dirs, 'android-sdk-license'), "w+" ) as f:
        f.write("\n8933bad161af4178b1185d1a37fbf41ea5269c55")
        f.write("\nd56f5187479451eabf01fb78af6dfcb131a6481e")

    sdkmanager = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"),  "tools/bin/sdkmanager")
    Utils.runCmd('%s --update > /dev/null' % (sdkmanager, ) )
    
    #update android sdk
    has_ndk_bundle = False
    if "components" in config:
        components = config["components"]
        
        # is has ndk-bundle
        if "ndk-bundle" not in components:
            has_ndk_bundle = True


        componentsStr = " ".join( '"%s"'%(v, ) for v in components)
        cmd = 'echo "y" | %s   %s > /dev/null' % (sdkmanager,  componentsStr)
        Utils.runCmd(cmd)

    #配置NDK
    if "ndk" in config and config["ndk"] !=  None:
        ndk_url =  config["ndk"] 

        android_ndk_zip_name = "ndk.zip"
        
        #判断本地的ndk
        needDownload  = True
        android_sdk_zip = "android_sdk.zip"
        if os.path.isfile(android_sdk_zip) and ("ndk_sha_256" in config) and config["ndk_sha_256"] != None:
            sha256 = Utils.sha256_checksum(android_sdk_zip)
            if sha256.lower() == config["ndk_sha_256"]:
                needDownload =  False
        #需要下载NDK
        if needDownload:
            Utils.download(ndk_url, android_ndk_zip_name)
        #解压NDK
        Utils.extractZipFile(android_ndk_zip_name,  "./android_ndk")
        
        #获取NDK真实的地址
        extractZipFilePath = os.path.realpath("./android_ndk")
        extractZipFilePath_dir_list = os.listdir(extractZipFilePath)
        list_len = len(extractZipFilePath_dir_list)
        if list_len <= 0:
            return  False
       
        NDK_ROOT = os.path.join(extractZipFilePath, extractZipFilePath_dir_list[list_len - 1] )
        Utils.setOSEnviron("NDK_ROOT", NDK_ROOT)       
    else:
        #如果没有配置NDK，也没有设置下载sdkmanager
        if not has_ndk_bundle:
            componentsStr = '"ndk-bundle"'
            cmd = 'echo "y" | %s   %s > /dev/null' % (sdkmanager,  componentsStr)
            Utils.runCmd(cmd)

        #默认使用ndk-bundle的ndk        
        Utils.setOSEnviron("NDK_ROOT", os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "ndk-bundle"))

    #打印ndk版本
    NDK_ROOT = os.environ["NDK_ROOT"]
    with open(os.path.join(NDK_ROOT, "source.properties")) as f:
        for  line in  f.readlines(): 
            v = line.split('=')
            if len(v) != 2:
                continue
            key = v[0].strip()  
            if key == "Pkg.Revision":
                value = v[1].strip()
                print "NDK Version:%s" %(value,)
                break