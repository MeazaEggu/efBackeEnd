from common.source import Sources
from common.pattern import Patterns
import os
import re
import io
import requests
import json
from flask import jsonify
import shutil

from flask import Flask
from flask_apscheduler import APScheduler

class ImportDataFromFileService:
    """JOBS = [
        {
            'id': 'importdatafromfile',
            'func': 'jobs:self.import_data',
            'args': (),
            'trigger': 'interval',
            'seconds': 10
        }
    ]"""

    """SCHEDULER_API_ENABLED = True
    scheduler = APScheduler()"""

    def get_atm_type(self, EJ):
        if (re.match(Patterns.DIEBOLD_ATM_LOG_FILE_NAME_PATTERN, EJ)):
            return 'DIEBOLD'
        elif (re.match(Patterns.NCR_ATM_LOG_FILE_NAME_PATTERN,EJ)):
            return 'NCR'
        else:
            return None
    def split_to_list(self, file_path,atm_type):
        try:
            with io.open(file_path, mode="r", encoding="utf8", errors='') as fd:
                content = fd.read()
            full_text = re.sub(r'[^\x00-\x7F]+|[\x1b]+|[\x00]+', ' ', content)
            ej_list=[]
            if(atm_type=='NCR'):
                matches = re.finditer(Patterns.NCR_ATM_LOG_FILE_SINGLE_TRANSACTION_PATTERN, full_text, re.MULTILINE)
                for matche in matches:
                    ej_list.append(matche.group())
                return ej_list#full_text.split(Patterns.NCR_ATM_LOG_SPLIT_TRANSACTION_PATTERN)
            elif(atm_type=='DIEBOLD'):
                matches = re.finditer(Patterns.DIEBOLD_ATM_LOG_FILE_SINGLE_TRANSACTION_PATTERN, full_text, re.MULTILINE)
                for matche in matches:
                    ej_list.append(matche.group())
                return ej_list#full_text.split(Patterns.DIEBOLD_ATM_LOG_SPLIT_TRANSACTION_PATTERN)
            else:
                return ej_list
        except Exception as ex:
            return None
    def send_transaction_to_elastic_search(self,logs,bank,atm,atm_type):
        #INSERT DATA=ROW/DOCUMENT AT BANK=DATABASE/INDEX AND ATM=TABLE/TYPE
        total_logs=len(logs)
        success_logs=0
        error_logs=0
        for log in logs:
            url=Sources.ELASTIC_SEACRH_URL+"/"+bank+"_temp/"+"atm"
            request_elastic_search = requests.post(url, json={"atm_type":str(atm_type),"atm":str(atm),"log": str(log)})
            response_json=request_elastic_search.json()
            if request_elastic_search.status_code in [200,201]:
                success_logs=success_logs+1
                print("++++++++++++++++++++++++++++++++++++++++"+str(request_elastic_search.content))
            else:
                error_logs=error_logs+1
                print("----------------------------------------"+str(request_elastic_search.content))
        return dict({"total_logs":total_logs,"success_logs":success_logs, "error_logs":error_logs})
    def move_ej(self,from_path,destination):
        to_path=destination[0]+"/"+destination[1]+"/"+destination[2]+"/"
        #To_path source dir
        if (os.path.exists(destination[0]+"/")):
            # Bank dir
            if (os.path.exists(destination[0]+"/"+destination[1]+"/")):
                # atm dir
                if (os.path.exists(destination[0]+"/"+destination[1]+"/"+destination[2]+"/")):
                    pass
                else:
                    os.mkdir(destination[0]+"/"+destination[1]+"/"+destination[2]+"/");
            else:
                os.mkdir(destination[0]+"/"+destination[1]+"/");
                if (os.path.exists(destination[0]+"/"+destination[1]+"/"+destination[2]+"/")):
                    pass
                else:
                    os.mkdir(destination[0]+"/"+destination[1]+"/"+destination[2]+"/");
        else:
            os.mkdir(destination[0])
            if(os.path.exists(destination[0]+"/"+destination[1]+"/")):
                if(os.path.exists(destination[0]+"/"+destination[1]+"/"+destination[2]+"/")):
                    pass
                else:
                    os.mkdir(destination[0]+"/"+destination[1]+"/"+destination[2]+"/")
            else:
                os.mkdir(destination[0]+"/"+destination[1]+"/")
                if (os.path.exists(destination[0] + "/" + destination[1] + "/" + destination[2] + "/")):
                    pass
                else:
                    os.mkdir(destination[0] + "/" + destination[1] + "/" + destination[2] + "/")
        print(shutil.move(from_path, to_path))

    #@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
    def start(self):
        bank_name=""
        atm_name=""
        banks = [banks_dir for banks_dir in os.listdir(Sources.FTP_FILE_SOURCE)]# if os.path.isfile(f)]
        print(banks)
        for bank in banks:
            bank_name=bank
            atms = [atm_dir for atm_dir in os.listdir(Sources.FTP_FILE_SOURCE+"/"+bank_name)]
            for atm in atms:
                atm_name=atm
                #GET EJ LOG FILES IN THE DIRECTORY
                EJs = [EJ_dir for EJ_dir in os.listdir(Sources.FTP_FILE_SOURCE +"/"+ bank_name +"/"+ atm_name)]

                #EJ_read_status=True
                for EJ in EJs:
                    #NAVIGATE TO SINGLE EJ LOG FILE
                    atm_type=self.get_atm_type(str(EJ))
                    if atm_type:
                        ej_list=self.split_to_list(Sources.FTP_FILE_SOURCE +"/"+ bank_name +"/"+ atm_name+"/"+EJ, atm_type)
                        if ej_list:
                            send_transaction_to_elastic_search_response=self.send_transaction_to_elastic_search(logs=ej_list,bank=bank,atm=atm,atm_type=atm_type)
                            #MOVE FILE
                            #print(send_transaction_to_elastic_search_response)
                            if send_transaction_to_elastic_search_response["total_logs"]!=send_transaction_to_elastic_search_response["error_logs"]:
                                self.move_ej(Sources.FTP_FILE_SOURCE + "/" + bank_name + "/" + atm_name + "/" + EJ,
                                             [Sources.DIRECTORY_TO_MOVE,bank_name,atm_name,EJ])
                                print(send_transaction_to_elastic_search_response)
                                print(Sources.FTP_FILE_SOURCE + "/" + bank_name + "/" + atm_name + "/" + EJ)
                            else:
                                pass

                #end ej file iteration
                #break
            #end atms itration
            #break
        #end bank itration
"""
findall	Returns a list containing all matches
search	Returns a Match object if there is a match anywhere in the string
split	Returns a list where the string has been split at each match
sub	Replaces one or many matches with a string
"""
#return ''.join([i if ord(i) < 128 else ' ' for i in text])

"""
import os
import shutil

os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
"""