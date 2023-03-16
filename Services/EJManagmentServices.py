
from common.databases import Connections
from model.All import Banks
from common.source import Sources
import requests
from model.All import ATMs
class EJManagmentServices:
    def __init__(self):
        pass

    def listEJByATMId(self,atmpyload,current_user):
        db_session=None
        try:
            atmId=None
            print("yesss")
            start,max,size=0,0,0
            tempBank=None
            if atmpyload:
                if "atm" in atmpyload:
                    if "id" in atmpyload["atm"]:
                        atmId=atmpyload['atm']["id"]
                    else:
                        message = "ATM not found1"
                        #return {"message": message,"status":False}, 404
                        return {"message": message, "ejs": None, "status": False, "size": 0, "start": start,
                                "max": max}, 404
                else:
                    message = "ATM not found"
                    return {"message": message, "ejs": None, "status": False, "size": 0, "start": start, "max": max}, 404

            else:
                message = "ATM not found"
                return {"message": message, "ejs": None, "status": False, "size": 0, "start": start, "max": max}, 404

            db_session = Connections().get_connection()
            #bank = db_session.query(Banks).get(current_user.bank_id)
            if current_user.privilage.usertype == "pss" and atmId!=None and atmId!=0:
                atm=db_session.query(ATMs).get(atmId)
                if atm:
                    bank = db_session.query(Banks).get(atm.bank_id)
                else:
                    message = "ATM not found"
                    return {"message": message, "ejs": None, "status": False, "size": 0, "start": start,"max": max}, 404

            if current_user.privilage.usertype == "bank":
                bank = db_session.query(Banks).get(current_user.bank_id)

            if bank:
                bank_name=bank.name
                atm = db_session.query(ATMs).filter(ATMs.bank_id == bank.id).first()
                if atm:
                    atmName=atm.name
                    print("atm Id ==== ATM name", str(atmId)+" "+str(atmName))
                    url=Sources.ELASTIC_SEACRH_URL+"/"+bank_name+"/"+Sources.ELASTIC_SEACRH_URL_TYPE_NAME+"/_search?size=10000"
                    print(url)
                    ejQueryFromElasticSearch={"query": {"match": {"atm": atmName}} }
                    response=requests.get(url=url,json=ejQueryFromElasticSearch)
                    print(response)
                    print(response.status_code)
                    print(int(response.status_code))
                    if response.status_code in [200,201]:
                        print("200 201")
                        ejs=response.json()['hits']['hits']
                        print("Ej ========")
                        print(ejs)
                        message="Success"
                        start=atmpyload["start"]
                        max=atmpyload["max"]

                        if start == 0 and max == 0:
                            pass
                        elif start == 0 and max != 0:
                            ejs = ejs[:max]
                        elif start != 0 and max == 0:
                            ejs = ejs[start:]
                        elif start != 0 and max != 0:
                            if start + max > start + max:
                                ejs = ejs[start:len(ejs)]
                            else:
                                ejs = ejs[start:start + max]
                        else:
                            pass

                        #return {"message": message,"ejs":[ejs],"status":True}, 201
                        return {"message": message, "ejs": ejs, "status": True, "size": len(ejs), "start": start,"max": max}, 201
                    else:
                        message="Request failed try again"
                        return {"message": response.json(), "ejs": None, "status": False, "size": 0, "start": start,"max": max}, 501
                else:
                    message="ATM not found"
                    return {"message": message, "ejs": None, "status": False, "size": 0, "start": start,"max": max}, 404
            else:
                message="Bank not found"
                #return {"message": message,"status":False}, 404
                return {"message": message, "ejs": None, "status": False, "size": 0, "start": start,"max": max}, 404
        except Exception as ex:
            return {"message": str(ex), "ejs": None, "status": False, "size": 0, "start": start, "max": max}, 501

        finally:
            del(db_session)




    def listEJByBankIdAndATMId(self,payload,current_user):
        atmId = None
        bankId = None
        atm=None
        bank=None
        start,max,size=0,0,0
        if payload:
            if "atm" in payload:
                if "id" in payload["atm"]:
                    atmId = payload["atm"]["id"]
                    if atmId <= 0:
                        message = "ATM not found"
                        return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
                    else:
                        atm = ATMs(id=payload["atm"]["id"])
                else:
                    message = "ATM not found"
                    return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
            else:
                message = "ATM not found"
                return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404

            if "bank" in payload:
                if "id" in payload["bank"]:
                    bank=Banks(id=payload["bank"]["id"])
                else:
                    message = "Bank not found"
                    return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
            else:
                message = "Bank not found"
                return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
        else:
            message = "ATM or Bank not found"
            return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
        db_session = Connections().get_connection()
        bank = db_session.query(Banks).get(bank.id)
        if bank:
            atm = db_session.query(ATMs).get(atm.id)
            if atm:
                url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
                ejQueryFromElasticSearch = {"query": {"match": {"atm": atm.name}}}
                response = requests.get(url=url, json=ejQueryFromElasticSearch)
                if response.status_code in [200, 201]:
                    ejs = response.json()['hits']['hits']
                    start = payload["start"]
                    max = payload["max"]

                    if start == 0 and max == 0:
                        pass
                    elif start == 0 and max != 0:
                        ejs = ejs[:max]
                    elif start != 0 and max == 0:
                        ejs = ejs[start:]
                    elif start != 0 and max != 0:
                        if start + max > start + max:
                            ejs = ejs[start:len(ejs)]
                        else:
                            ejs = ejs[start:start + max]
                    else:
                        pass

                    message = "Success"

                    return {"message": message, "ejs": ejs, "status":True, "size": len(ejs),"start":start,"max":max}, 201
                elif response.status_code in [404]:
                    message="Bank log cound not found"
                    return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 404
                elif response.status_code in [500,501]:
                    message = "Log repositery request error"
                    return {"message": message, "ejs": None, "status":False, "size": 0,"start":start,"max":max}, 501
                else:
                    message = "Request failed try again"
                    return {"message": response.json(), "ejs": None, "status": False, "size": 0, "start": start, "max": max}, 501
            else:
                message="ATM not found"
                return {"message": message, "ejs": None, "status": False, "size": 0, "start": start,"max": max}, 404
        else:
            message="Bank not found"
            return {"message": message, "ejs": None, "status": False, "size": 0, "start": start, "max": max}, 404



    def getCountTransactionSuccessByBankId(self, payload,current_user):
        atmId = None
        atm = None
        bank = None
        bankTemp=None
        bankId = None
        start,max,size=0,0,0
        print(payload["bank"]["id"])
        if payload:
            if "bank" in payload:
                if "id" in payload["bank"]:
                    bankId = payload["bank"]["id"]
                    if bankId <= 0:
                        message = "Bank not found"
                        return {"message": message}, 404
                    else:
                        bankTemp = Banks(id=payload["bank"]["id"])
                else:
                    message = "Bank not found"
                    return {"message": message, "count": 0, "status": False}, 404
            else:
                message = "Bank not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404

        db_session = Connections().get_connection()
        if current_user.privilage.usertype == "pss" and bankTemp!=None:
            # atm=db_session.query(ATMs).get(atm.id)
            bank = db_session.query(Banks).get(bankTemp.id)
        if current_user.privilage.usertype == "bank":
            bank = db_session.query(Banks).get(current_user.bank_id)

        if bank:
            url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
            ejQueryFromElasticSearch = {"query": {"match": {"response_status": 0}}}
            response = requests.get(url=url, json=ejQueryFromElasticSearch)
            if response.status_code in [200, 201]:
                ejs = response.json()['hits']['hits']
                message = "Success"
                return {"message": message, "count": len(ejs), "status":True}, 201
            elif response.status_code in [404]:
                message = "Bank log cound not found"
                return {"message": message, "count": 0, "status": False}, 404
            elif response.status_code in [500, 501]:
                message = "Log repositery request error"
                return {"message": message, "count": 0, "status": False}, 501
            else:
                message = "Request failed try again"
                return {"message": message, "count": 0, "status": False}, 501
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404

    def getCountTransactionFailedByBankId(self, payload,current_user):
        atmId = None
        atm = None
        bank = None
        bankId=None
        bankTemp=None
        print(payload["bank"]["id"])
        if payload:
            if "bank" in payload:
                if "id" in payload["bank"]:
                    bankId = payload["bank"]["id"]
                    if bankId <= 0:
                        message = "Bank not found"
                        return {"message": message}, 404
                    else:
                        bankTemp = Banks(id=payload["bank"]["id"])
                else:
                    message = "Bank not found"
                    return {"message": message, "count": 0, "status": False}, 404
            else:
                message = "Bank not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404



        db_session = Connections().get_connection()
        #bank = db_session.query(Banks).get(current_user.bank_id)
        if current_user.privilage.usertype=="pss" and bankTemp!=None:
            #atm=db_session.query(ATMs).get(atm.id)
            bank = db_session.query(Banks).get(bankTemp.id)
        if current_user.privilage.usertype=="bank":
            bank = db_session.query(Banks).get(current_user.bank_id)
        if bank:
            url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
            ejQueryFromElasticSearch = {"query": {"match": {"response_status": 1}}}
            print(url)
            response = requests.get(url=url, json=ejQueryFromElasticSearch)
            if response.status_code in [200, 201]:
                ejs = response.json()['hits']['hits']
                message = "Success"
                return {"message": message, "count": len(ejs), "status":True}, 201
            elif response.status_code in [404]:
                message = "Bank log cound not found"
                return {"message": message, "count": 0, "status": False}, 404
            elif response.status_code in [500, 501]:
                message = "Log repositery request error"
                return {"message": message, "count": 0, "status": False}, 501
            else:
                message = "Request failed try again"
                return {"message": response.json(), "count": 0, "status": False}, 501
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404

    def getCountTransactionSuccessByATMId(self, payload, current_user):
        atmId = None
        atm = None
        bank = None
        print(payload["atm"]["id"])
        if payload:
            if "atm" in payload:
                if "id" in payload["atm"]:
                    atmId = payload["atm"]["id"]
                    if atmId<=0:
                        message = "ATM not found"
                        return {"message": message, "count": 0, "status": False}, 404
                    else:
                        atm = ATMs(id=payload["atm"]["id"])
                else:
                    message = "ATM not found"
                    return {"message": message, "count": 0, "status": False}, 404
            else:
                message = "ATM not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "ATM or Bank not found"
            return {"message": message, "count": 0, "status": False}, 404

        db_session = Connections().get_connection()
        #IF PSS USER WORK ON ATM ID USE ATM BANK ID THEN GET THE EJ
        if current_user.privilage.usertype=="pss":
            atm=db_session.query(ATMs).get(atm.id)
            bank = db_session.query(Banks).get(atm.bank_id)
        if current_user.privilage.usertype=="bank":
            bank = db_session.query(Banks).get(current_user.bank_id)

        if bank:
            isAtmInBank = db_session.query(ATMs).filter(ATMs.bank_id == bank.id)
            atm = db_session.query(ATMs).get(atm.id)
            if atm and isAtmInBank:
                url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
                ejQueryFromElasticSearch={ "query": { "bool": { "must": [ { "match": { "response_status":0 }}, { "match": { "atm": "main" }} ] } } }
                response = requests.get(url=url, json=ejQueryFromElasticSearch)
                if response.status_code in [200, 201]:
                    ejs = response.json()['hits']['hits']
                    message = "Success"
                    return {"message": message, "count": len(ejs), "status": True}, 201
                elif response.status_code in [404]:
                    message = "Bank log cound not found"
                    return {"message": message, "count": 0, "status": False}, 404
                elif response.status_code in [500, 501]:
                    message = "Log repositery request error"
                    return {"message": message, "count": 0, "status": False}, 501
                else:
                    message = "Request failed try again"
                    return {"message": message, "count": 0, "status": False}, 501
            else:
                message = "ATM not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404


    def getCountTransactionFailedByATMId(self, payload,current_user):
        atmId = None
        atm = None
        bank = None
        if payload:
            if "atm" in payload:
                if "id" in payload["atm"]:
                    atmId = payload["atm"]["id"]
                    if atmId <= 0:
                        message = "ATM not found"
                        return {"message": message, "count": 0, "status": False}, 404
                    else:
                        atm = ATMs(id=payload["atm"]["id"])
                else:
                    message = "ATM not found"
                    return {"message": message, "count": 0, "status": False}, 404
            else:
                message = "ATM not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "ATM or Bank not found"
            return {"message": message, "count": 0, "status": False}, 404

        db_session = Connections().get_connection()
        #bank = db_session.query(Banks).get(current_user.bank_id)
        # IF PSS USER WORK ON ATM ID USE ATM BANK ID THEN GET THE EJ
        if current_user.privilage.usertype == "pss":
            atm = db_session.query(ATMs).get(atm.id)
            bank = db_session.query(Banks).get(atm.bank_id)
        if current_user.privilage.usertype == "bank":
            bank = db_session.query(Banks).get(current_user.bank_id)

        if bank:
            isAtmInBank = db_session.query(ATMs).filter(ATMs.bank_id == bank.id)
            atm = db_session.query(ATMs).get(atm.id)
            if atm and isAtmInBank:
                url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
                #ejQueryFromElasticSearch = { "query" : { "bool": { "should": [ { "match": { "response_status": 1 } }, { "match": { "atm": atm.name } } ]} } }
                ejQueryFromElasticSearch={ "query": { "bool": { "must": [ { "match": { "response_status":1 }}, { "match": { "atm": "main" }} ] } } }
                print(url)
                print(ejQueryFromElasticSearch)
                response = requests.get(url=url, json=ejQueryFromElasticSearch)
                if response.status_code in [200, 201]:
                    ejs = response.json()['hits']['hits']
                    message = "Success"
                    return {"message": message, "count": len(ejs), "status":True}, 201
                elif response.status_code in [404]:
                    message = "Bank log cound not found"
                    return {"message": message, "count": 0, "status": False}, 404
                elif response.status_code in [500, 501]:
                    message = "Log repositery request error"
                    return {"message": response.json(), "count": 0, "status": False}, 501
                else:
                    message = "Request failed try again"
                    return {"message": response.json(), "count": 0, "status": False}, 501
            else:
                message = "ATM not found"
                return {"message": message, "count": 0, "status": False}, 404
        else:
            message = "Bank not found"
            return {"message": message, "count": 0, "status": False}, 404




    def fillterByBankId(self, payload,current_user):
        response_code=payload["response_code"]
        response_status=payload["response_status"]
        users_bank=payload["users_bank"]
        atm=payload["atm"]
        atm_type=payload["atm_type"]
        ejQueryFromElasticSearch={'query': {'bool': {'must': []}}}
        isQueryParametrFound=False
        ejQueryBy=""
        db_session=Connections().get_connection()
        bank=None
        start,max,size=0,0,0
        if current_user.privilage.usertype=="bank":
            bank = db_session.query(Banks).get(current_user.bank_id)
            if bank:
                isQueryParametrFound=True
            else:
                message = "Bank log cound not found"
                return {"message": message, "ejs": None, "status": False}, 404
        elif current_user.privilage.usertype=="pss":
            if "bank" in payload:
                bankPayload = payload["bank"]
                if bankPayload:
                    if "id" in bankPayload:
                        bank = db_session.query(Banks).get(bankPayload["id"])
                        if bank:
                            """ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"bank": bank}})
                            isSearchParametrFound=True
                            ejQueryBy+="bank """
                            print("   found")
                            isQueryParametrFound=True
                        else:
                            message = "Bank log cound not found"
                            return {"message": message, "ejs": None, "start": start, "max": max, "size": 0,"status": False}, 404

                    else:
                        message = "Bank id key not found"
                        return {"message": message, "ejs": None, "start": start, "max": max, "size": 0,"status": False}, 404
                else:
                    message = "Bank key has no value"
                    return {"message": message, "ejs": None, "start": start, "max": max, "size": 0,"status": False}, 404
            else:
                message = "Bank key not found"
                return {"message": message, "ejs": None, "start": start, "max": max, "size": 0,"status": False}, 404
        else:
            message = "Bank ken not found"
            return {"message": message, "ejs": None, "start": start, "max": max, "size": 0,"status": False}, 404



        if "response_code" in payload:
            if payload["response_code"]:
                ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"response_code": payload["response_code"]}})
                isQueryParametrFound = True
                ejQueryBy += "response_code "
        if "response_status" in payload:
            if payload["response_status"]==0 or payload["response_status"]==1:
                ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"response_status": payload["response_status"]}})
                isQueryParametrFound = True
                ejQueryBy += "response_status "
        if "users_bank" in payload:
            if payload["users_bank"]:
                ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"users_bank": users_bank}})
                isQueryParametrFound = True
                ejQueryBy += "users_bank "
        if "atm" in payload:
            if payload["atm"]:
                atms = db_session.query(ATMs).filter(ATMs.id == payload["atm"]["id"], ATMs.bank_id==bank.id)
                print(payload["atm"]["id"])
                if atms.count()>0:
                    print(atms.count())
                    atm=atms.first()
                    ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"atm": atm.name}})
                    isQueryParametrFound = True
                    ejQueryBy += "atm "
                else:
                    pass
        if "atm_type" in payload:
            if payload["atm_type"]:
                ejQueryFromElasticSearch['query']['bool']['must'].append({"match": {"atm_type": atm_type}})
                isQueryParametrFound = True
                ejQueryBy += "atm_type "
        if isQueryParametrFound:
            url = Sources.ELASTIC_SEACRH_URL + "/" + bank.name + "/" + Sources.ELASTIC_SEACRH_URL_TYPE_NAME + "/_search?size=10000"
            response = requests.get(url=url, json=ejQueryFromElasticSearch)
            print(ejQueryFromElasticSearch)
            print(ejQueryBy)
            if response.status_code in [200, 201]:
                ejs = response.json()['hits']['hits']
                start=payload["start"]
                max = payload["max"]

                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    ejs=ejs[:max]
                elif start != 0 and max == 0:
                    ejs=ejs[start:]
                elif start != 0 and max != 0:
                    if start + max > start + max:
                        ejs = ejs[start:len(ejs)]
                    else:
                        ejs = ejs[start:start + max]
                else:
                    pass

                message = "Success"
                return {"message": message,"ejs":ejs ,"size": len(ejs),"start":start,"max":max, "status": True}, 201
            elif response.status_code in [404]:
                message = "Bank log cound not found"
                return {"message": message,"ejs":None ,"start":start,"max":max,"size":0, "status": True}, 404
            elif response.status_code in [500, 501]:
                message = "Log repositery request error"
                return {"message": message,"ejs":None ,"start":start,"max":max,"size":0, "status": True}, 501
            else:
                message = "Request failed try again"
                return {"message": message,"ejs":None ,"start":start,"max":max,"size":0, "status": True}, 501
        else:
            message = "Atleast one parametre need to fillter"
            return {"message": message,"ejs":None ,"start":start,"max":max,"size":0, "status": True}, 501