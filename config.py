#-*-coding:utf-8-*-

config ={
    "Android":{
        #sdk components
        "components":(
            "ndk-bundle",
            "cmake;3.6.4111459", 
        ),

        "ndk": 'https://dl.google.com/android/repository/android-ndk-r16b-linux-x86_64.zip',    #ndk下载地址

        "build_script":{
            "build_sxtwl":
            {
                'needBuild': True
            }
        },
    },
}


