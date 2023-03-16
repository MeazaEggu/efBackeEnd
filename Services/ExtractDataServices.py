

from common.source import Sources
from common.pattern import Patterns
from common.Logger import Logger
import re
import requests
import json
import threading
class ExtractDataServices:
    className="ExtractData"
    logger=Logger()
    def getIndex(self):
        indexs = []
        try:
            response_index_list=requests.get(Sources.ELASTIC_SEACRH_URL_LIST_INDEX, params={'format':'json','pretty':'true'})
            if response_index_list.status_code in [200,201]:
                index_list_json=response_index_list.json()
                for index in index_list_json:
                    if(re.match(Patterns.TEMP_INDEX_NAME_PATTERN, index['index'])):
                        indexs.append(str(index['index']))
                return indexs
            else:
                self.logger.logError(message=str("Index not found"), className=self.className, methodName="getIndex")
        except Exception as ex:
            self.logger.logDebug(message=str(ex),className=self.className,methodName="getIndex")
        return indexs


    def getSequenceNumber(self,atm_type,atm_log):
        sequence_number = None
        try:
            if atm_type=="NCR":
                sequence_number_line=re.search(Patterns.NCR_ATM_LOG_LINE_SEQUENCE_NUMBER_PATTERN, atm_log, re.MULTILINE)
                if(sequence_number_line):
                    sequence_number = re.search(Patterns.NCR_ATM_LOG_SEQUENCE_NUMBER_PATTERN, sequence_number_line.group(), re.MULTILINE)
                    if(sequence_number):
                        sequence_number=sequence_number.group()
                    else:
                        self.logger.logError(message=str(
                            "Sequence number could not found [No match text] ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                                             className=self.className, methodName="getSequenceNumber")
                        sequence_number = None#"no mach for n"
                else:
                    self.logger.logError(message=str(
                        "Sequence number could not found [Not match line] ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                                         className=self.className, methodName="getSequenceNumber")
            elif atm_type=="DIEBOLD":
                sequence_number_line = re.search(Patterns.DIEBOLD_ATM_LOG_LINE_SEQUENCE_NUMBER_PATTERN, atm_log, re.MULTILINE)
                if (sequence_number_line):
                    sequence_number = re.search(Patterns.DIEBOLD_ATM_LOG_SEQUENCE_NUMBER_PATTERN,
                                                     sequence_number_line.group(), re.MULTILINE)
                    if (sequence_number):
                        sequence_number = sequence_number.group().replace("[Host Seq.No.:","").replace(" ","").replace("]","")
                    else:
                        self.logger.logError(message=str("Sequence number could not found [No match text] ATM type:"+atm_type+" --- log:{"+atm_log+"}"), className=self.className, methodName="getSequenceNumber")
                        sequence_number = None#"no mach for d"
                else:
                    self.logger.logError(message=str("Sequence number could not found [Not match line] ATM type:"+atm_type+" --- log:{"+atm_log+"}"), className=self.className,methodName="getSequenceNumber")
                    sequence_number = None#"no match line D"
            else:
                self.logger.logError(message=str("Sequence number could not found [Invalid ATM type] ATM type:"+atm_type+" --- log:{"+atm_log+"}"), className=self.className,methodName="getSequenceNumber")
                sequence_number = None#"ATM type"
            return sequence_number
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getSequenceNumber")
        return sequence_number

    def getStartAndEndTransactionDateTime(self,atm_type,atm_log):
        start_and_end_date_time_list = {"start_transaction_date_time": "", "end_transaction_date_time": ""}
        try:

            if atm_type=="NCR":
                start_transaction_date_time = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_START_DATE_TIME_PATTERN, atm_log,
                                                        re.MULTILINE)
                if (start_transaction_date_time):
                    start_and_end_date_time_list["start_transaction_date_time"]=start_transaction_date_time.group().replace("DATE ", "").replace("    TIME ", " ")
                else:
                    self.logger.logError(message=str(
                        "Start transaction datetime not match ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                                         className=self.className, methodName="getStartAndEndTransactionDateTime")

                end_transaction_date_time = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_END_DATE_TIME_PATTERN, atm_log,
                                                        re.MULTILINE)
                if (end_transaction_date_time):
                    start_and_end_date_time_list["end_transaction_date_time"] = end_transaction_date_time.group().replace(" TRANSACTION END","")
                else:
                    self.logger.logError(message=str(
                        "End transaction datetime not match ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getStartAndEndTransactionDateTime")
                return start_and_end_date_time_list

            elif atm_type=="DIEBOLD":
                start_transaction_date_time = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_START_DATE_TIME_PATTERN, atm_log,
                                                        re.MULTILINE)
                if (start_transaction_date_time):
                    start_and_end_date_time_list["start_transaction_date_time"] = start_transaction_date_time.group().replace(" Card Inserted","")
                else:
                    self.logger.logError(message=str(
                        "Start transaction datetime not match ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getStartAndEndTransactionDateTime")

                end_transaction_date_time = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_END_DATE_TIME_PATTERN, atm_log,
                                                      re.MULTILINE)
                if (end_transaction_date_time):
                    start_and_end_date_time_list["end_transaction_date_time"] =end_transaction_date_time.group().replace(" RESPONSE","").replace(" Card Ejected","")
                else:
                    self.logger.logError(message=str(
                        "Start transaction datetime not match ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getStartAndEndTransactionDateTime")
                return start_and_end_date_time_list
            else:
                self.logger.logError(message=str(
                    "Invalid atm type :" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getStartAndEndTransactionDateTime")
                return start_and_end_date_time_list
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getStartAndEndTransactionDateTime")
        return start_and_end_date_time_list

    def getAmount(self, atm_type, atm_log):
        amount = None
        try:
            if atm_type == "NCR":
                amount_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_AMOUNT_PATTERN, atm_log,
                                        re.MULTILINE)
                if (amount_line):
                    amount = amount_line.group().split("(")[2]
                else:
                    self.logger.logError(message=str(
                        "Not match amount ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAmount")
            elif atm_type == "DIEBOLD":
                amount_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_AMOUNT_PATTERN, atm_log,
                                        re.MULTILINE)
                if (amount_line):
                    amount = amount_line.group().replace("ETB", "").replace("AMOUNT :", "")
                else:
                    self.logger.logError(message=str(
                        "Not match amount ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAmount")
            else:
                self.logger.logError(message=str(
                    "Invalid ATM type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getAmount")
            return amount
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getAmount")
        return amount
    def getResponse(self,atm_type,atm_log):
        response_list = {"response_status": "", "response_code": "", "response_message": ""}
        try:

            if atm_type == "NCR":
                response_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_RESPONSE_PATTERN, atm_log,
                                                        re.MULTILINE)
                if (response_line):
                    response=response_line.group().replace("(1RESPONSE : (","")
                    response_list["response_code"]=re.search(r"\d{2,3}\s{1}\d{2,3}",response).group().split(" ")[1]
                    response_list["response_message"] = re.sub(r"\d{2,3}\s{1}\d{2,3}", "", response)
                    #response_status=0
                    if response_list["response_code"]=="00" or response =="APPROVED OR COMPLETED SUCCESSFULLY":
                        response_list["response_status"]=0
                    else:
                        response_list["response_status"]=1
                else:
                    self.logger.logError(message=str(
                        "Not match response ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getResponse")
            elif atm_type == "DIEBOLD":
                response_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_RESPONSE_PATTERN, atm_log,
                                          re.MULTILINE)
                if (response_line):
                    response = response_line.group().replace("RESPONSE :","")
                    response_list["response_code"] = re.search(r"\d{1,2}\s{1}\d{2,3}", response).group().split(" ")[1]
                    response_list["response_message"] = re.sub(r"\d{1,2}\s{1}\d{2,3}", "", response)
                    # response_status=0
                    if response_list["response_code"] == "00" or response == "APPROVED OR COMPLETED SUCCESSFULLY.":
                        response_list["response_status"] = 0
                    else:
                        response_list["response_status"] = 1
                else:
                    self.logger.logError(message=str(
                        "Not match response ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getResponse")
            else:
                self.logger.logError(message=str(
                    "Invalid ATM type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getResponse")
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getResponse")

        return response_list

    def getTransactionType(self, atm_type, atm_log):
        transaction_type=""
        try:
            if atm_type == "NCR":
                transaction_type_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_TYPE_PATTERN, atm_log,
                                                        re.MULTILINE)
                if transaction_type_line:
                    transaction_type=transaction_type_line.group()
                else:
                    self.logger.logError(message=str(
                        "Not match transaction type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getTransactionType")
            elif atm_type == "DIEBOLD":
                transaction_type_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_TYPE_PATTERN, atm_log,
                                                        re.MULTILINE)
                if transaction_type_line:
                    transaction_type=transaction_type_line.group()
                else:
                    self.logger.logError(message=str(
                        "Not match transaction type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getTransactionType")
            else:
                self.logger.logError(message=str(
                    "Invalid ATM type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getTransactionType")
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getTransactionType")
        return transaction_type

    def getCardNumber(self, atm_type, atm_log):
        card_number=""
        try:
            if atm_type == "NCR":
                card_number_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_CARD_NUMBER_PATTERN, atm_log,
                                             re.MULTILINE)
                if card_number_line:
                    card_number = card_number_line.group()
                else:
                    self.logger.logError(message=str(
                        "Not match card number type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getCardNumber")
            elif atm_type == "DIEBOLD":
                card_number_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_CARD_NUMBER_PATTERN, atm_log,
                                                  re.MULTILINE)
                if card_number_line:
                    card_number = card_number_line.group()
                else:
                    self.logger.logError(message=str(
                        "Not match card number type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getCardNumber")
            else:
                self.logger.logError(message=str(
                    "Invalid ATM type ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getCardNumber")
        except Exception as ex:
            self.logger.logDebug(message=str(ex)+" "+"ATM type:"+atm_type+" --- log:{"+atm_log+"}", className=self.className, methodName="getCardNumber")
        return card_number

    def getUsersBank(self,atm_type,card_number):
        users_bank="None"
        #print("1 -----",card_number)
        bank_list = {
            "415104": "Commercial Bank of Ethiopia", "9231414": "Bunna International Bank", "9231405": "Dashen Bank",
             "9231411": "Lion International Bank", "9231418": "Debub Global Bank", "9231419": "Enat Bank",
             "9231407": "Wegagen Bank", "379987": "Dashen Bank", "585972": "Bank of Abyssinia", "960100": "Abay Bank",
             "9231413": "Oromia International Bank", "458543": "Wegagen Bank", "458554": "Wegagen Bank",
             "458805": "Wegagen Bank", "534394": "Wegagen Bank", "923151": "Wegagen Bank", "424311": "Dashen Bank",
             "502285": "Zemen Bank", "458571": "Commercial Bank of Ethiopia", "458300": "Commercial Bank of Ethiopia",
             "475194": "Commercial Bank of Ethiopia", "419715": "Commercial Bank of Ethiopia",
             "471297": "Commercial Bank of Ethiopia", "431997": "Commercial Bank of Ethiopia",
             "419714": "Commercial Bank of Ethiopia", "465372": "Commercial Bank of Ethiopia", "957105": "AdIB",
             "956905": "AIB", "956909": "AIB", "956915": "AIB", "957005": "BrIB", "957015": "BRIB", "957209": "CBO",
             "957205": "CBO", "956805": "NIB", "956809": "NIB", "956808": "NIB", "956806": "NIB", "956807": "NIB",
             "956715": "UB", "956705": "UB", "956704": "UB", "956709": "UB", "956706": "UB"}
        try:
            if card_number:

                users_bank_match=re.search(r"\d{5,8}", card_number)
                if users_bank_match!=None:
                    if users_bank_match.group(0) in bank_list:
                        users_bank=bank_list[users_bank_match.group(0)]
                    else:
                        self.logger.logError(message=str(
                            "Not match card number prefix ATM type:" + atm_type + " --- log:{" + "atm_log" +  " card  number:{"+str(card_number)+"}"),
                            className=self.className, methodName="getCardNumber")
                    """else:
                        self.logger.logError(message=str(
                            "Not match card number type ATM type:" + atm_type + " --- log:{" + "atm_log" + " card  number:{" + str(
                                card_number) + "}"),
                            className=self.className, methodName="getCardNumber")"""
                else:
                    card_number_split=card_number.split("X")

                    if len(card_number)>0:
                        if card_number_split[0] in bank_list:
                            users_bank = bank_list[card_number_split[0]]
                        else:
                            pass
                    else:
                        pass
            else:
                self.logger.logError(message=str(
                    "Card number is none ATM type:" + atm_type + " --- log:{" + "atm_log" + " card  number:{" + str(
                        card_number) + "}"),
                    className=self.className, methodName="getCardNumber")
        except Exception as ex:
            self.logger.logDebug(message=str(ex) + " " + "ATM type:" + atm_type + " --- log:{" + "atm_log" + " card  number:{"+str(card_number)+"}}",
                                 className=self.className, methodName="getCardNumber")
        return users_bank

    def getAuthNumber(self, atm_type, atm_log):
        auth_number=""
        try:
            if atm_type == "NCR":
                auth_number_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_AUTH_NUMB_PATTERN, atm_log,
                                             re.MULTILINE)
                if auth_number_line:
                    auth_number = auth_number_line.group().replace("1AUTH NUMB:","").replace("(","")
                else:
                    self.logger.logError(message=str(
                        "Not match auth_number ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAuthNumber")
            elif atm_type == "DIEBOLD":
                auth_number_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_AUTH_NUMB_PATTERN, atm_log,
                                                  re.MULTILINE)
                if auth_number_line:
                    auth_number = auth_number_line.group().replace("AUTH NUMB:","")
                else:
                    self.logger.logError(message=str(
                        "Not match auth_number ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAuthNumber")
            else:
                self.logger.logError(message=str(
                    "Not match auth_number ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getAuthNumber")
        except Exception as ex:
            self.logger.logDebug(
                message=str(ex) + " " + "ATM type:" + atm_type + " --- log:{" + atm_log + "}}",
                className=self.className, methodName="getAuthNumber")
        return auth_number

    def getAccount(self, atm_type, atm_log):
        account=""
        try:
            if atm_type == "NCR":
                account_line = re.search(Patterns.NCR_ATM_LOG_TRANSACTION_ACCOUNT_PATTERN, atm_log,
                                             re.MULTILINE)
                if account_line:
                    account = account_line.group().replace("(1ACCOUNT: (","")
                else:
                    self.logger.logError(message=str(
                        "Not match Account number ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAccount")
            elif atm_type == "DIEBOLD":
                account_line = re.search(Patterns.DIEBOLD_ATM_LOG_TRANSACTION_ACCOUNT_PATTERN, atm_log,
                                                  re.MULTILINE)
                if account_line:
                    account = account_line.group().replace("ACCOUNT:","")
                else:
                    self.logger.logError(message=str(
                        "Not match Account number ATM type:" + atm_type + " --- log:{" + atm_log + "}"),
                        className=self.className, methodName="getAccount")
            else:
                self.logger.logError(message=str(
                    "Invalid ATM type ATM type: " + atm_type + " --- log:{" + atm_log + "}"),
                    className=self.className, methodName="getAccount")
        except Exception as ex:
            self.logger.logDebug(
                message=str(ex) + " " + "ATM type:" + atm_type + " --- log:{" + atm_log + "}}",
                className=self.className, methodName="getAccount")
        return account

    def parssing(self, document_id,document_index,document_data_atm_type,document_data_atm,document_data_log):
        transaction={}
        try:
            transaction["id"] = document_id
            transaction["sequence_number"] = self.getSequenceNumber(document_data_atm_type, document_data_log)
            #print("+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+--+-+-+-+_+--")
            print(transaction["sequence_number"])
            transaction["transaction_type"] = self.getTransactionType(document_data_atm_type, document_data_log)
            if(transaction["sequence_number"] and transaction["transaction_type"]!="BALANCE INQUIRY"):
                #Change new index name by removing _temp
                transaction["bank"] = document_index.replace("_temp","")
                transaction["atm"] = document_data_atm
                transaction["atm_type"] = document_data_atm_type

                start_and_end_transaction_date_time=self.getStartAndEndTransactionDateTime(document_data_atm_type, document_data_log)
                transaction["start_transaction_date_time"]=start_and_end_transaction_date_time["start_transaction_date_time"]
                transaction["end_transaction_date_time"] = start_and_end_transaction_date_time["end_transaction_date_time"]

                transaction["transaction_type"] = self.getTransactionType(document_data_atm_type, document_data_log)
                transaction["card_number"]=self.getCardNumber(document_data_atm_type, document_data_log)
                transaction["users_bank"]=self.getUsersBank(atm_type=transaction["atm_type"],card_number=transaction["card_number"])
                transaction["account"] = self.getAccount(document_data_atm_type, document_data_log)
                transaction["auth_number"]=self.getAuthNumber(document_data_atm_type, document_data_log)

                response=self.getResponse(document_data_atm_type, document_data_log)
                transaction["response_status"]=response["response_status"]
                transaction["response_code"] = response["response_code"]
                transaction["response_message"] = response["response_message"]

                transaction["amount"]=self.getAmount(document_data_atm_type, document_data_log)
                transaction["detail"]=document_data_log
                print("withdraal")
                return transaction
            elif transaction["transaction_type"]=="BALANCE INQUIRY":
                transaction["bank"] = document_index.replace("_temp", "")
                transaction["atm"] = document_data_atm
                transaction["atm_type"] = document_data_atm_type

                start_and_end_transaction_date_time = self.getStartAndEndTransactionDateTime(document_data_atm_type,
                                                                                             document_data_log)
                transaction["start_transaction_date_time"] = start_and_end_transaction_date_time[
                    "start_transaction_date_time"]
                transaction["end_transaction_date_time"] = start_and_end_transaction_date_time[
                    "end_transaction_date_time"]

                #transaction["transaction_type"] = self.getTransactionType(document_data_atm_type, document_data_log)
                transaction["card_number"] = self.getCardNumber(document_data_atm_type, document_data_log)
                transaction["users_bank"] = self.getUsersBank(atm_type=transaction["atm_type"],
                                                              card_number=transaction["card_number"])
                transaction["account"] = self.getAccount(document_data_atm_type, document_data_log)
                transaction["auth_number"] = self.getAuthNumber(document_data_atm_type, document_data_log)

                #response = self.getResponse(document_data_atm_type, document_data_log)
                transaction["response_status"] = None
                transaction["response_code"] = None
                transaction["response_message"] = None

                transaction["amount"] = None#self.getAmount(document_data_atm_type, document_data_log)
                transaction["detail"] = document_data_log
                print("balance inquiry")
                return transaction
            else:
                self.logger.logError(
                    message="Sequence number not match/ found / value=None " + "ATM type:" + document_data_atm_type + " --- log:{" + document_data_log + "} --- atm:{" +
                            document_data_atm_type + " ---  document_id: {" + str(
                        document_id) + "} --- document_index: {" + str(
                        document_index) + "} --- document_data_atm:{" + document_data_atm + "} }}",
                    className=self.className, methodName="parssing")
                return False
        except Exception as ex:
            self.logger.logDebug(
                message=str(ex) + " " + "ATM type:" + document_data_atm_type + " --- log:{" + document_data_log + "} --- atm:{"+
                        document_data_atm_type+" ---  document_id: {"+str(document_id)+"} --- document_index: {"+str(document_index)+"} --- document_data_atm:{"+document_data_atm+"} }}",
                className=self.className, methodName="parssing")
            return False
        #print(transaction)


    def delete_type(self,delete_url,json):
        try:
            #delete_url = Sources.ELASTIC_SEACRH_URL + "/" + index + "/_delete_by_query"
            requests.post(delete_url,json=json)
        except Exception as ex:
            pass



    def insertIntoELK(self,Document):
        print("yeeeeessss")
        print(Document)
        # CHECK IF SINGLE TRANSACTION HAS THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] AND SEQUENCE_NUMBER MUST HAS A VALUE
        if ('bank' in Document) and ('sequence_number' in Document) and (Document["sequence_number"] != None):
            insert_url = Sources.ELASTIC_SEACRH_URL + "/" + Document["bank"] + "/atm"
            insert_document_request = requests.post(insert_url, json=Document)
            print("inser to elk")
            print(insert_document_request)
            if insert_document_request.status_code in [200, 201]:
                # response_json = request_elastic_search.json()
                # delete from [index]_temp index
                delete_url = Sources.ELASTIC_SEACRH_URL + "/" + Document["bank"] + "_temp/_delete_by_query"
                self.delete_type(delete_url=delete_url,json={"query": {"match": {"_id": Document["id"]}}})
                delete_document_request = requests.post(delete_url,
                                                        json={"query": {"match": {"_id": Document["id"]}}})
                # print(delete_document_request.content)
                return True

            else:
                # UNABLE TO INSERT DATA TO ELK
                self.logger.logError(
                    message="UNABLE TO INSERT DATA TO ELK " +
                            "uri: " + insert_url + " response content: " + insert_document_request.content + " status code: " + insert_document_request.status_code,
                    className=self.className, methodName="loadUnformatedData")
                return False
        elif ('bank' in Document) and (not ('sequence_number' in Document) or not (Document["sequence_number"] != None)):

            delete_url = Sources.ELASTIC_SEACRH_URL + "/" + Document["bank"] + "_temp/_delete_by_query"
            delete_document_request = requests.post(delete_url, json={"query": {"match": {"_id": Document["id"]}}})
            # print(delete_document_request.content)
            self.logger.logInfo(
                message="Delete transaction not having indexs [bank,sequence_number] " + " id: " + str(
                    Document["id"]) +
                        "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                className=self.className, methodName="loadUnformatedData")
            return False

        else:
            # NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE
            # delete_document_request = requests.post(url, json={"query": {"match": {"_id": transaction["id"]}}})

            delete_url = Sources.ELASTIC_SEACRH_URL + "/" + Document["bank"] + "_temp/_delete_by_query"
            delete_document_request = requests.post(delete_url,
                                                    json={"query": {"match": {"_id": Document["id"]}}})
                                                    
            self.logger.logInfo(
                message="NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE" + " id: " + str(
                    Document["id"]) +
                        "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                className=self.className, methodName="loadUnformatedData")
            return False

    def loadUnformatedData(self):
        #print("indexs")
        transactions=[]
        transactions_id=[]
        indexs=self.getIndex()

        #CHECK INDEXS ARE EXIST
        try:
            if(indexs):
                for index in indexs:
                    response_document_list=requests.get(Sources.ELASTIC_SEACRH_URL_LIST_DOCUMET+"/"+index+"/_search", json={"size":5000})
                    if response_document_list.status_code in [200,201]:
                        ##GET DOCUMENT LIST FROM response_document_list
                        document_list=response_document_list.json()["hits"]["hits"]
                        if len(document_list)>=1:
                            #CHECK IF LIST SIZE CONTAIN ELEMENTS
                            for document in document_list:
                                document_id=document["_id"]
                                document_index=document["_index"]
                                document_score=document["_score"]
                                document_data = document["_source"]
                                if("atm_type" in document_data) and ("atm" in document_data) and ("log" in document_data):
                                    print(document_data)
                                    document_data_atm_type =document_data["atm_type"]
                                    document_data_atm = document_data["atm"]
                                    document_data_log = document_data["log"]
                                    #PARSS AND APPEND TO THE LIST
                                    parssingResult=self.parssing(document_id, document_index, document_data_atm_type,document_data_atm, document_data_log)
                                    if parssingResult==False:
                                        print("NOT APPEND   "+str(len(transactions)))
                                    else:
                                        transactions.append(parssingResult)
                                        #print("APPPPPPEEEENNNNDDDD"+str(len(transactions)))
                                else:
                                    #DELETE FEATCHED TRANSACTION WHICH HAS NO HAS THE FOLLOWING INDEX [ATM_TYPE,ATM,LOG]
                                    delete_url = Sources.ELASTIC_SEACRH_URL + "/" + document_index + "/_delete_by_query"
                                    delete_document_request = requests.post(delete_url, json={"query": {"match": {"_id": document_id}}})
                                    self.logger.logInfo(
                                        message="DELETE FEATCHED TRANSACTION WHICH HAS NO HAS THE FOLLOWING INDEX [ATM_TYPE,ATM,LOG]"+
                                        "uri: "+delete_url+" response content: "+delete_document_request.content+" status code: "+delete_document_request.status_code,
                                        className=self.className, methodName="loadUnformatedData")
                        else:
                            #NOTING TO DO BECAUSE OF REQUESTED INDEX HAS NO DATA ELEMENT IN ["hits"]["hits"]
                            self.logger.logError(
                                message="Index has no data element index:{"+index+"} --- document_list:{"+"document_list"+"}}",
                                className=self.className, methodName="loadUnformatedData")
                    else:
                        self.logger.logError(
                            message="ELK not response success  content:{" + response_document_list.content + " --- status_code:{" + response_document_list.status_code + "}}",
                            className=self.className, methodName="loadUnformatedData")
                        #NOTING TO DO BECAUSE OF REQUESTED URL NOT RETURN RESPONSE CODE [200 OR 201]
                        #hits->total->value
                        #hits->hits[{ "_index","_type","_id","_score","_source": {"atm_type": 1,"log":1,"atm":1} }]
            else:
                # NOTING TO DO BECAUSE OF EVEN SINGLE INDEX IS NOT FOUND
                self.logger.logError(
                    message="Index not found",
                    className=self.className, methodName="loadUnformatedData")
        except Exception as ex:
            self.logger.logDebug(
                message=str(ex),
                className=self.className, methodName="loadUnformatedData")


        #print(transactions)
        success=0
        total=0
        failed=0
        try:
            print("start count",len(transactions))
            count=0
            '''for i in range(0,len(transactions)):
                transaction=transactions[i]
                if ('bank' in transaction) and ('sequence_number' in transaction) and (transaction["sequence_number"] != None):
                    count+=1
                    insert_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "/atm"
                    insert_document_request = requests.post(insert_url, json=transaction)
                    print("inser to elk")
                    print(insert_url)
                    print(transaction)
                    if insert_document_request.status_code in [200, 201]:
                        success=success+1
                        total=total+1
                        #response_json = request_elastic_search.json()
                        #delete from [index]_temp index
                        delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                        delete_document_request = requests.post(delete_url, json={"query": {"match": {"_id": transaction["id"] } }})
                    else:
                        #UNABLE TO INSERT DATA TO ELK
                        self.logger.logError(
                            message="UNABLE TO INSERT DATA TO ELK " +
                                    "uri: " + insert_url + " response content: " + insert_document_request.content + " status code: " + insert_document_request.status_code,
                            className=self.className, methodName="loadUnformatedData")
                        failed=failed+1
                        total = total+1
                elif ('bank' in transaction) and (not ('sequence_number' in transaction) or not (transaction["sequence_number"] != None)):
                    delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                    delete_document_request = requests.post(delete_url,json={"query": {"match": {"_id": transaction["id"]}}})
                    #print(delete_document_request.content)
                    self.logger.logInfo(
                        message="Delete transaction not having indexs [bank,sequence_number] " + " id: "+str(transaction["id"])+
                                "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                        className=self.className, methodName="loadUnformatedData")
                    failed = failed + 1
                    total = total + 1
                else:
                    # NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE
                    # delete_document_request = requests.post(url, json={"query": {"match": {"_id": transaction["id"]}}})
                    delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                    delete_document_request = requests.post(delete_url,
                                                            json={"query": {"match": {"_id": transaction["id"]}}})
                    self.logger.logInfo(
                        message="NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE" + " id: " + str(
                            transaction["id"]) +
                                "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                        className=self.className, methodName="loadUnformatedData")
                    failed = failed + 1
                    total = total + 1
'''







            #print(count)
            #ITERATE THROUGH PARSSED TRANSACTION
            for transaction in transactions:
                insertResult=self.insertIntoELK(transaction)
                if insertResult==True:
                    success+=1
                    total += 1
                else:
                    failed+=1
                    total+=1

                '''print("yeeeeessss")
                print(transaction)
                #CHECK IF SINGLE TRANSACTION HAS THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] AND SEQUENCE_NUMBER MUST HAS A VALUE
                if ('bank' in transaction) and ('sequence_number' in transaction) and (transaction["sequence_number"]!=None):
                    insert_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "/atm"
                    insert_document_request = requests.post(insert_url,json=transaction)
                    print("inser to elk")
                    print(insert_document_request)
                    if insert_document_request.status_code in [200, 201]:
                        success=success+1
                        total=total+1
                        #response_json = request_elastic_search.json()
                        #delete from [index]_temp index
                        delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                        delete_document_request = requests.post(delete_url, json={"query": {"match": {"_id": transaction["id"] } }})
                        #print(delete_document_request.content)

                    else:
                        #UNABLE TO INSERT DATA TO ELK
                        self.logger.logError(
                            message="UNABLE TO INSERT DATA TO ELK " +
                                    "uri: " + insert_url + " response content: " + insert_document_request.content + " status code: " + insert_document_request.status_code,
                            className=self.className, methodName="loadUnformatedData")
                        failed=failed+1
                        total = total+1
                elif ('bank' in transaction) and (not ('sequence_number' in transaction) or not (transaction["sequence_number"] != None)):
                    delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                    delete_document_request = requests.post(delete_url,json={"query": {"match": {"_id": transaction["id"]}}})
                    #print(delete_document_request.content)
                    self.logger.logInfo(
                        message="Delete transaction not having indexs [bank,sequence_number] " + " id: "+str(transaction["id"])+
                                "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                        className=self.className, methodName="loadUnformatedData")
                    failed = failed + 1
                    total = total + 1
                else:
                    #NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE
                    #delete_document_request = requests.post(url, json={"query": {"match": {"_id": transaction["id"]}}})
                    delete_url = Sources.ELASTIC_SEACRH_URL + "/" + transaction["bank"] + "_temp/_delete_by_query"
                    delete_document_request = requests.post(delete_url,
                                                            json={"query": {"match": {"_id": transaction["id"]}}})
                    self.logger.logInfo(
                        message="NOTHING TO DO BE CAUSE A TRANSACTION HAS NOT THE FOLLOWING KEYS[BANK,SEQUENCE_NUMBER] OR SEQUENCE_NUMBER MUST HAS A VALUE" + " id: " + str(
                            transaction["id"]) +
                                "uri: " + delete_url + " response content: " + delete_document_request.content + " status code: " + delete_document_request.status_code,
                        className=self.className, methodName="loadUnformatedData")
                    failed = failed + 1
                    total = total + 1'''
            print(success, failed, total)



        except Exception as ex:
            self.logger.logDebug(
                message=str(ex),
                className=self.className, methodName="loadUnformatedData")
        return dict({"total": total, "success": success, "failed": failed})




    def start(self):
        self.logger.logInfo(
            message="ANymessage",className="self.className", methodName="loadUnformatedData")
        print(self.loadUnformatedData())
        """formatted_transactions,formatted_transactions_id=self.load_unformated_data()
        print(formatted_transactions)
        print(formatted_transactions_id)"""
        #print(self.load_unformated_data())
        #load_unformated_data
            # get_index
            # parssing
                # get_sequence_number
                # get_start_and_end_transaction_date_time
                # atm_type
                # get_amount
                # get_response_list
                    #code
                    #message
                    #status 1/0 failed/success
                #Operation

        #elk load messed data and load to elk


        # INSERT DATA=ROW/DOCUMENT AT BANK=DATABASE/INDEX AND ATM=TABLE/TYPE
        #http://196.188.28.222:9200/_cat/indices
        #http://196.188.28.222:9200/testindex/_search?pretty=true
        #http://196.188.28.222:9200/_cat/indices?format=json&pretty=true


#extract_data=ExtractDataServices()
#print(extract_data.getUsersBank("DIEBOLD","458300XXXXXX7782"))