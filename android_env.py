#-*-coding:utf-8-*-

import os
from utils import Utils

def do_config(config):
    before_install_cmds   =(
        r"export TERM=dumb",
        r"touch ~/.android/repositories.cfg",
        r"mkdir -p /usr/local/android-sdk/licenses",
        r'echo -e "\n8933bad161af4178b1185d1a37fbf41ea5269c55" > /usr/local/android-sdk/licenses/android-sdk-license',
        r'echo -e "\nd56f5187479451eabf01fb78af6dfcb131a6481e" >> /usr/local/android-sdk/licenses/android-sdk-license',
    
        # Install NDK and cmake via android sdkmanager.
        r'export ANDROID_SDK_ROOT=/usr/local/android-sdk'
        r'/usr/local/android-sdk/tools/bin/sdkmanager --update > /dev/null'
        #'echo "y" | /usr/local/android-sdk/tools/bin/sdkmanager  "ndk-bundle" "cmake;3.6.4111459" > /dev/null'
    )

    for cmd in before_install_cmds:
        os.system(cmd)

    #update android sdk
    has_ndk_bundle = False
    if "components" in config:
        components = config["components"]
        
        if "ndk-bundle" not in components:
            has_ndk_bundle = True

        cmd = 'echo "y" | /usr/local/android-sdk/tools/bin/sdkmanager  %s > /dev/null' % ( " ".join( '"%s"'%(v, ) for v in components) ,)
        os.system(cmd)

    
    #配置NDK
    if "ndk" in config and config["ndk"] !=  None:
        ndk_url =  config["ndk"] 

        android_ndk_zip_name = "ndk.zip"
        Utils.download(ndk_url, android_ndk_zip_name)
        Utils.extractZipFile(android_ndk_zip_name,  "./android_ndk")
        cmd = "export NDK_ROOT=%s" %(os.path.realpath("./android_ndk"), )
        os.system(cmd)  
    else:
        #如果没有配置NDK，也没有设置下载sdkmanager
        if not has_ndk_bundle:
            cmd = 'echo "y" | /usr/local/android-sdk/tools/bin/sdkmanager %s > /dev/null' % ('"ndk-bundle"' ,)
            os.system(cmd)

        #默认使用ndk-bundle的ndk
        cmd = "export NDK_ROOT=/usr/local/android-sdk/ndk-bundle" 
        os.system(cmd)


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