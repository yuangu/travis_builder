#-*-coding:utf-8-*-

import os
from utils import Utils


def do_config(config):
    has_ndk_bundle = False
    
    #更新android sdk
    if Utils.getOSEnviron("ANDROID_SDK_ROOT") != None:
        Utils.setOSEnviron("TERM", "dumb")
        #Utils.setOSEnviron("ANDROID_SDK_ROOT", "/usr/local/android-sdk")

        Utils.runCmd("touch ~/.android/repositories.cfg")
        android_sdk_licenses_dirs = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "licenses")
        Utils.mkDir( android_sdk_licenses_dirs )
        
        with open( os.path.join(android_sdk_licenses_dirs, 'android-sdk-license'), "w+" ) as f:
            f.write("\n8933bad161af4178b1185d1a37fbf41ea5269c55")
            f.write("\nd56f5187479451eabf01fb78af6dfcb131a6481e")

        sdkmanager = os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"),  "tools/bin/sdkmanager")
        Utils.runCmd('%s --update > /dev/null' % (sdkmanager, ) )
    
        #update android sdk
        if "components" in config:
            components = config["components"]
            
            # is has ndk-bundle
            if "ndk-bundle" not in components:
                has_ndk_bundle = True


            componentsStr = " ".join( '"%s"'%(v, ) for v in components)
            cmd = 'echo "y" | %s   %s > /dev/null' % (sdkmanager,  componentsStr)
            Utils.runCmd(cmd)

    #更新NDK配置NDK
    if "ndk" in config and config["ndk"] !=  None:
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
        Utils.runCmd("chmod -R 775 %s"%(NDK_ROOT,))
        Utils.setOSEnviron("ANDROID_NDK_ROOT", NDK_ROOT)       
    else:
        #如果没有配置NDK，也没有设置下载sdkmanager
        if not has_ndk_bundle:
            componentsStr = '"ndk-bundle"'
            cmd = 'echo "y" | %s   %s > /dev/null' % (sdkmanager,  componentsStr)
            Utils.runCmd(cmd)

        #默认使用ndk-bundle的ndk        
        Utils.setOSEnviron("ANDROID_NDK_ROOT", os.path.join(Utils.getOSEnviron("ANDROID_SDK_ROOT"), "ndk-bundle"))

    #打印ndk版本
    NDK_ROOT = os.environ["ANDROID_NDK_ROOT"]
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



if __name__ == "__main__":
    config = {
        "ndk": 'https://dl.google.com/android/repository/android-ndk-r16b-linux-x86_64.zip',    #ndk下载地址
        "ndk_sha_1":'42aa43aae89a50d1c66c3f9fdecd676936da6128',
    }

    do_config(config)