#-*-coding:utf-8-*-
# coded by yuangu(lifulinghan@aol.com)
import os
import sys
sys.path.append("..")
from utils import Utils
import platform

class Android:
    mSDKRoot = None
    mNDKRoot = None
    
    def __init__(self):
        self.mNDKRoot = self.getNDKRoot()
        self.mSDKRoot = self.getSDKRoot()
        
        if self.mSDKRoot == None:
            self.mSDKRoot = self.downloadSDK()
        self.configSDK()
        
        if self.mNDKRoot == None: 
            self.mNDKRoot = os.path.join(self.mSDKRoot, "ndk-bundle")

    # 判断SDK是否含有cmake部分
    def hasCmake(self, ANDROID_SDK):
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

    #判断SDK是否含有NDK部分
    def hasNDK(self, ANDROID_SDK):
        ndk_properties = os.path.join(ANDROID_SDK, "ndk-bundle/source.properties")
        if os.path.exists(ndk_properties ):
            return True
        return False

    #判断package的版本号
    def getPackageVersion(self, packPath):
        if not os.path.isfile(os.path.join(packPath, "source.properties")):
            return None

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

    # 获取环境变量里的NDK
    def getNDKRoot(self):
        ndkOSEnvironKey = ["NDK_ROOT", "ANDROID_NDK_ROOT"]
        for k in ndkOSEnvironKey:
            v = Utils.getOSEnviron(k)
            if v != None:
                return v

        return None

    # 获取环境变量里的SDK路径
    def getSDKRoot(self):
        sdkOSEnvironKey = ["ANDROID_SDK_ROOT", "ANDROID_HOME"]
        for k in sdkOSEnvironKey:
            v = Utils.getOSEnviron(k)
            if v != None:
                return v

        return None

    # 下载安装SDK
    def downloadSDK(self):
        platformName = platform.system().lower()
        if platformName == 'macos':
            platformName = 'darwin'

        sdk_url = "https://dl.google.com/android/repository/sdk-tools-%s-4333796.zip" % (platformName, )

        sha256 = {
            'windows':'7e81d69c303e47a4f0e748a6352d85cd0c8fd90a5a95ae4e076b5e5f960d3c7a',
            'linux':'92ffee5a1d98d856634e8b71132e8a95d96c83a63fde1099be3d86df3106def9',
            'darwin': 'ecb29358bc0f13d7c2fa0f9290135a5b608e38434aad9bf7067d0252c160853e'
        }

        #判断本地的ndk
        needDownload  = True
        android_sdk_zip = "android_sdk.zip"    
        if os.path.isfile(android_sdk_zip) and sha256[platformName] != None:
            sha1 = Utils.sha256_checksum(android_sdk_zip)        
            if sha1.lower() == sha256[platformName]:
                print "exist %s" %(android_sdk_zip, )
                needDownload =  False

        #需要下载NDK
        if needDownload:
            Utils.download(sdk_url, android_sdk_zip)
            print "download %s" %(sdk_url, )

        #解压NDK
        Utils.cleanFile("./android_sdk")
        Utils.extractZipFile(android_sdk_zip,  "./android_sdk")
        
        #获取SDK真实的地址
        SDK_ROOT =  os.path.realpath("./android_sdk")
       
        #在linux机器上可能会有权限问题
        if "windows" != platform.system().lower():
            Utils.runCmd("chmod -R 775 %s"%(SDK_ROOT,))

        Utils.setOSEnviron("ANDROID_SDK_ROOT", SDK_ROOT) 
        return SDK_ROOT

    #配置SDK
    def configSDK(self):
        if self.mSDKRoot == None: 
            return False

        components = []

        #检查cmake的配置
        if not self.hasCmake(self.mSDKRoot):
            components.append("cmake;3.10.2.4988404")
        
        #检查NDK
        if self.mNDKRoot == None and not self.getPackageVersion(os.path.join(self.mSDKRoot, "ndk-bundle")):
            components.append("ndk-bundle")

        #判断有没有android-16的
        if not self.getPackageVersion(os.path.join(self.mSDKRoot, "platforms/android-16")):
            components.append("platforms;android-16")

        #update android sdk
        if  len(components) > 0:
            Utils.setOSEnviron("TERM", "dumb")        
            repositories = None

            #保存repositories.cfg的存在
            if "windows" == platform.system().lower():              
                repositories = os.path.join(os.environ['USERPROFILE'],  '.android/repositories.cfg')     
            else:           
                repositories = os.path.join(os.environ['HOME'],  '.android/repositories.cfg')
         
            Utils.mkDir(os.path.dirname(repositories))
            with open( repositories, "w+" ) as f:
                pass    
            
            #创建licenses
            android_sdk_licenses_dirs = os.path.join(self.mSDKRoot, "licenses")
            Utils.mkDir( android_sdk_licenses_dirs )
            
            with open( os.path.join(android_sdk_licenses_dirs, 'android-sdk-license'), "w+" ) as f:
                f.write("\nd56f5187479451eabf01fb78af6dfcb131a6481e")
                f.write("\n24333f8a63b6825ea9c5514f83c2829b004d1fee")

            sdkmanager = os.path.join(self.mSDKRoot,  "tools/bin/sdkmanager")
            if "windows" == platform.system().lower():
                sdkmanager = os.path.join(self.mSDKRoot,  r"tools\bin\sdkmanager")

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

    def getCmakeDir(self):
        ndk_cmake_dir  = os.path.join(self.mSDKRoot,  "cmake")
        if  not  os.path.isdir(ndk_cmake_dir):
            return None
        
        cmake_dir_list = os.listdir(ndk_cmake_dir)
        list_len = len(cmake_dir_list)
        if list_len <= 0:
            return  None
        
        return os.path.join(ndk_cmake_dir, cmake_dir_list[list_len - 1] )

    def getCmakeBin(self):
        CMAKE_DIR = self.getCmakeDir()
        ANDROID_CMAKE = os.path.join(self.getCmakeDir(), 'bin/cmake')
        return  ANDROID_CMAKE

    def getCmakeArg(self, build_type='Release', abi= 'armeabi-v7a', android_api_level = 16):
        CMAKE_DIR = self.getCmakeDir()
        ANDROID_CMAKE = os.path.join(self.getCmakeDir(), 'bin/cmake')
        ANDROID_NINJA=os.path.join(CMAKE_DIR,'bin/ninja')

        cmd = '''-DANDROID_ABI=%s \
            -DANDROID_PLATFORM=%s \
            -DCMAKE_BUILD_TYPE=%s \
            -DANDROID_NDK=%s \
            -DCMAKE_CXX_FLAGS=-std=c++11 -frtti -fexceptions \
            -DCMAKE_TOOLCHAIN_FILE=%s/build/cmake/android.toolchain.cmake \
            -DCMAKE_MAKE_PROGRAM=%s -G "Ninja" '''%(abi,android_api_level,build_type,self.mNDKRoot,self.mNDKRoot,ANDROID_NINJA) 
        
        return cmd
  
if __name__ == "__main__":
    android = Android()
    print android.getCmakeBin()