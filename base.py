# coding: utf8
# Author: tingjun/wei
# Data: 2018年6月12日
import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from enum import Enum



LOG_ROOT_DIRECTORY = 'F:\\python_logging'     #设置日志文件根目录

class Enum(Enum):
    """
    返回代码统一整理
    """
    res_success = '10000'   #成功
    res_part_success = '10003'  #部分成功，部分失败
    res_fail = '10006'  #失败
    res_param_empty = '10009'   #参数为空
    res_param_missing = '10012'    #参数缺失
    res_param_is_not_file = '10015'     #上传的不是文件
    res_not_support_file_type = '10018'     #不支持的文件类型


class LogHandler(logging.Logger):
    """
    日志分片类
    stream ：控制是否打印日志到控制台
    files：控制是否写入日志文件
    level：日志登记
    prefixName：日志前缀名称，格式为 frefixName + '_' + 20180703 + '.log'，如：log_20180703.log
    """
    def __init__(self,prefixName='log',level = 'DEBUG',stream = False,files = True):
        self.name = prefixName
        self.level = level
        logging.Logger.__init__(self,self.name,level=self.level)
        if files:
            self.__file_handler(self.level)
        if stream:
            self.__stream_handler(self.level)

    def __file_handler(self,level = None):      #存入日志文件
        log_name = os.path.join(LOG_ROOT_DIRECTORY,self.name + '_' + time.strftime('%Y%m%d') + '.log')
        handler  = TimedRotatingFileHandler(log_name,
                                            when = 'D',
                                            interval = 1,
                                            backupCount = 0)
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(pathname)s [line:%(lineno)d]\n%(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def __stream_handler(self,level = None):        #控制台输出
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(pathname)s [line:%(lineno)d]%(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(level)
        self.addHandler(handler)
