from common.databases import Connections
from model.All import ATMs
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
            if atmpyload:
                if "id" in atmpyload:
                    atmId=atmpyload["id"]
                else:
                    message = "ATM not found"
                    return {"message": message}, 404
            else:
                message = "ATM not found"
                return {"message": message}, 404

            db_session = Connections().get_connection()
            bank = db_session.query(Banks).get(current_user.bank_id)
            if bank:
                bank_name=bank.name
                atm = db_session.query(ATMs).filter(ATMs.bank_id == current_user.bank_id).first()
                if atm:
                    atmName=atm.name
                    print("atm Id ==== ATM name", str(atmId)+" "+str(atmName))
                    url=Sources.ELASTIC_SEACRH_URL+"/"+bank_name+"/"+Sources.ELASTIC_SEACRH_URL_TYPE_NAME+"/_search?size=10000"
                    ejQueryFromElasticSearch={"query": {"match": {"atm": atmName}} }
                    response=requests.get(url=url,json=ejQueryFromElasticSearch)
                    if response.status_code in [200,201]:
                        ejs=response.json()['hits']['hits']
                        print("Ej ========")
                        print(ejs)
                        message="Success"

                        return {"message": message,"ejs":[ejs]}, 201
                    else:
                        message="Request failed try again"
                        return {"message": response.content,"ejs":None}, 501
                else:
                    message="ATM not found"
                    return {"message": message}, 404
            else:
                message="Bank not found"
                return {"message": message}, 404
        except Exception as ex:
            return {"message": str(ex)}, 501
        finally:
            del(db_session)




    def listEJByBankIdAndATMId(self,payload,current_user):
        atmId = None
        bankId = None
        atm=None
        bank=None
        if payload:
            if "atm" in payload:
                if "id" in payload["atm"]:
                    # atmId = payload["atm"]["id"]
                    atm = ATMs(id=payload["atm"]["id"])
                else:
                    message = "ATM not found"
                    return {"message": message}, 404
            else:
                message = "ATM not found"
                return {"message": message}, 404
            if "bank" in payload:
                if "id" in payload["bank"]:
                    bank=Banks(id=payload["bank"]["id"])
                else:
                    message = "Bank not found"
                    return {"message": message}, 404
            else:
                message = "Bank not found"
                return {"message": message}, 404
        else:
            message = "ATM or Bank not found"
            return {"message": message}, 404
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
                    message = "Success"

                    return {"message": message, "ejs": ejs}, 201
                elif response.status_code in [404]:
                    message="Bank log cound not found"
                    return {"message": message, "ejs": None}, 404
                elif response.status_code in [500,501]:
                    message = "Log repositery request error"
                    return {"message": message, "ejs": None}, 501
                else:
                    message = "Request failed try again"
                    return {"message": response.content, "ejs": None}, 501
            else:
                message="ATM not found"
                return {"message": message, "ejs": None}, 404
        else:
            message="Bank not found"
            return {"message": message, "ejs": None}, 404