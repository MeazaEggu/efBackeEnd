import logging
import os
from common.source import Sources
#from common.Logger import Logger
logging.basicConfig(handlers=[logging.FileHandler(filename=Sources.LOG_FILE_PATH,encoding='utf-8', mode='a+')],format="%(asctime)s %(name)s:%(levelname)s:%(message)s",datefmt="%F %A %T")

#logging.basicConfig(filename='logger.log', encoding='utf-8')#level=logging.DEBUG)
class Logger:
    def logError(self,message,className,methodName):
        logging.error("Class: %s --- Method: %s --- Message: %s ",className,methodName,message)
    def logInfo(self,message,className,methodName):
        logging.info("Class: %s --- Method: %s --- Message: %s ",className,methodName,message)
    def logDebug(self,message,className,methodName):
        logging.debug("Class: %s --- Method: %s --- Message: %s ",className,methodName,message)