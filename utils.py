#-*-coding:utf-8-*-

import os
import shutil
import zipfile
import hashlib
import sys
import platform
import urllib
import subprocess


#下载进度条回调 
def callbackfunc(blocknum, blocksize, totalsize):
    pass 
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    # percent = 100.0 * blocknum * blocksize / totalsize
    # if percent > 100:
    #     percent = 100
    
    # max_arrow = 50 #进度条的长度
    # num_arrow = int(percent * max_arrow/100.0) 

    # process_bar = '\r[' + '>' * num_arrow + '#' * (max_arrow -  num_arrow) + ']'\
    #                   + '%.2f%%' % percent  #带输出的字符串，'\r'表示不换行回到最左边
    # sys.stdout.write(process_bar) #这两句打印字符到终端
    # sys.stdout.flush()


#工具类
class Utils():
    #如果目录不存，则创建。
    @staticmethod
    def mkDir(dirPath):
        if os.path.exists(dirPath) and os.path.isdir(dirPath):
            return
        parent = os.path.dirname(dirPath)
        if not (os.path.exists(parent) and os.path.isdir(parent)):
            Utils.mkDir(parent)
        
        os.mkdir(dirPath)
    
    #获取某个目录是否含有某个文件, extList获取指定的文件后缀
    @staticmethod
    def getAllDirFiles(dirPath, extList = None):
        ret = []    
        for file in os.listdir( dirPath):
            if os.path.isfile(os.path.join(dirPath, file)):
               ret.append(os.path.join(dirPath, file))
            else:
                ret += Utils.getAllDirFiles(os.path.join(dirPath, file))
        
        #需要过滤某些文件
        if extList != None:             
            extList = [tmp.lower() for tmp in extList]           
            ret = [path for path in ret if os.path.splitext(path)[1].lower()  in extList]    
        return ret

    #清理掉某个数据
    @staticmethod
    def cleanFile(path):
        if not os.path.exists(path):
            return
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    #将一个文件夹压缩成zip文件
    @staticmethod
    def makeZipFile(fileName, fromDir):        
        fileList = Utils.getAllDirFiles(fromDir)
        with zipfile.ZipFile(fileName , 'w')  as zip:
            for file in fileList:
                zip.write(file, os.path.relpath(file, fromDir))
    
    @staticmethod
    def extractZipFile(fileName, toDir = "."):
        file_zip = zipfile.ZipFile(fileName, 'r')
        for file in file_zip.namelist():
            file_zip.extract(file, toDir)
        file_zip.close()
            

    @staticmethod
    def sha256_checksum(filename, block_size=65536):
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def sha1_checksum(filename, block_size=65536):
        sha1 = hashlib.sha1()        
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha1.update(block)
        return sha1.hexdigest()

    @staticmethod
    def download(url, path):
        urllib.urlretrieve(url, path, callbackfunc)

    @staticmethod
    def setOSEnviron(key, vaule):
        os.environ[key] = vaule

    @staticmethod
    def getOSEnviron(key):
        if key in os.environ.keys():
            return os.environ[key]
        return None

    @staticmethod
    def runCmd(cmd):
        print cmd
        return os.system(cmd) == 0
