#-*-coding:utf-8-*-

config ={
    "Android":{
        #sdk components
        "components":(
            "ndk-bundle",
            #"cmake;3.6.4111459", 
        ),

        "ndk": 'https://dl.google.com/android/repository/android-ndk-r16b-linux-x86_64.zip',    #ndk下载地址
        "ndk_sha_256":'92ffee5a1d98d856634e8b71132e8a95d96c83a63fde1099be3d86df3106def9', 

        "build_script":{
            "build_sxtwl":
            {
                'needBuild': True
            }
        },
    },
}


