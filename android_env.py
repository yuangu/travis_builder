#-*-coding:utf-8-*-

import os
from utils import Utils

def config_env(config):
    before_install_cmds   =(
        "export TERM=dumb",
        "touch ~/.android/repositories.cfg",
        "mkdir -p /usr/local/android-sdk/licenses",
        'echo -e "\n8933bad161af4178b1185d1a37fbf41ea5269c55" > /usr/local/android-sdk/licenses/android-sdk-license',
        'echo -e "\nd56f5187479451eabf01fb78af6dfcb131a6481e" >> /usr/local/android-sdk/licenses/android-sdk-license',
    
        # Install NDK and cmake via android sdkmanager.
        'export ANDROID_SDK_ROOT=/usr/local/android-sdk'
        '/usr/local/android-sdk/tools/bin/sdkmanager --update > /dev/null'
        #'echo "y" | /usr/local/android-sdk/tools/bin/sdkmanager  "ndk-bundle" "cmake;3.6.4111459" > /dev/null'
    )

    for cmd in before_install_cmds:
        os.system(cmd)

    #update android sdk
    if "components" in config:
        components = config["components"]

        cmd = 'echo "y" | /usr/local/android-sdk/tools/bin/sdkmanager   %s > /dev/null' % ( " ".join( '%s'%(v, ) for v in components) ,)
        os.system(cmd)

        #默认使用ndk-bundle的ndk
        cmd = "export NDK_ROOT=/usr/local/android-sdk/ndk-bundle" 
        os.system(cmd)

    #使用下载的ndk
    if "ndk" in config:
        ndk_url =  config["ndk"] 
        if ndk_url != None:
            android_ndk_zip_name = "ndk.zip"
            Utils.download(ndk_url, android_ndk_zip_name)
            Utils.extractZipFile(android_ndk_zip_name,  "./android_ndk")
            cmd = "export NDK_ROOT=%s" %(os.path.realpath("android_ndk"), )
            os.system(cmd)
            


