# -*- coding: utf-8 -*-

#sample usage starts：

#import Logger


#logger1 = Logger.Logger('test.log',logging.DEBUG ,logging.DEBUG)
#logger1.debug('this%s',' is that')
#logger1.debug('single this')

# sample ends

import logging
 
class Logger:
 def __init__(self, path,clevel = logging.DEBUG,Flevel = logging.DEBUG):
  self.logger = logging.getLogger(path)

  self.logger.setLevel(logging.DEBUG)
  fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
  #设置CMD日志
  sh = logging.StreamHandler()
  sh.setFormatter(fmt)
  sh.setLevel(clevel)
  if not self.logger.handlers:
  #设置文件日志
      fh = logging.FileHandler(path)
      fh.setFormatter(fmt)
      fh.setLevel(Flevel)
      self.logger.removeHandler(sh)
      self.logger.removeHandler(fh)
      self.logger.addHandler(sh)
      self.logger.addHandler(fh)

  
 def debug(self,msg,*args,**kwargs):
  self.logger.debug(msg, *args, **kwargs)
  
 def info(self,message,*args, **kwargs):
  self.logger.info(message)
 
 def warn(self,message,*args, **kwargs):
  self.logger.warn(message, *args, **kwargs)
 
 def error(self,message,*args, **kwargs):
  self.logger.error(message, *args, **kwargs)
 
 def critical(self,message,*args, **kwargs):
  self.logger.critical(message, *args, **kwargs)
