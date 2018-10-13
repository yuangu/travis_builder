#-*-coding:utf-8-*-

config ={
    #android打包配置项
    "Android":{
        #sdk components
        "components":[
            #"ndk-bundle",
            #"cmake;3.6.4111459", 
        ],

        #"ndk": 'https://dl.google.com/android/repository/android-ndk-r16b-linux-x86_64.zip',    #ndk下载地址
        #"ndk_sha_1":'42aa43aae89a50d1c66c3f9fdecd676936da6128', 

        "build_script":{
            "build_sxtwl":
            {                   
                'needBuild': False,
                 "abiList" : [
                    #'armeabi', 
                    'armeabi-v7a',
                    "arm64-v8a",
                    "x86",
                    'x86_64',
                    # 'mips',
                    # 'mips64',
                ]
            },

            "build_curl":
            {                   
                'needBuild': True,
                'version':'7.61.1', #curl的版本
                'cmake_arguments':"-DCMAKE_USE_OPENSSL=0 -DHTTP_ONLY=1 -DBUILD_SHARED_LIBS=0",
                "abiList" : [
                    #'armeabi', 
                    'armeabi-v7a',
                    "arm64-v8a",
                    "x86",
                    'x86_64',
                    # 'mips',
                    # 'mips64',
                ]
            }
        },



    },


    'use_send_firefox':True,   #如果使用邮箱的附件的话，设置成false
    #邮件发送的地址
    #帐号和密码来源https://github.com/normal-four/test/blob/815393a266142ba64df0402f9a6c15c203b95156/spider/mailtest.py
    'mail':
    {
        'try_time':0, 
        
        'smtp_username' : "wzp_test@126.com",
        'smtp_passwd' : "a1269325139",
        'smtp_server' : 'smtp.126.com',
        'to_mail': "1143402671@qq.com"
    }
}


