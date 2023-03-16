from common.databases import Connections
from model.All import Users
from model.All import Banks
from passlib.hash import sha256_crypt
import jwt
from functools import wraps
from flask import request
class BankManagmentServices:
    def __init__(self,bankRequestDTO):
        if bankRequestDTO!=None:
            self.bank = Banks(
                name=bankRequestDTO['name'],
            )

    def save(self,current_user):
        db_session = None
        message=None
        bank=[]
        try:
            db_session = Connections().get_connection()
            checkBankExist = db_session.query(Banks).filter(Banks.name == self.bank.name).count()
            if checkBankExist >= 1:
                message = "This bank name alrady registred"
                return {"message": message, "banks": None, 'status': False}, 501

            bank=self.bank
            bank.id=None
            #bank.bank=current_user.bank
            db_session.add(bank)
            db_session.commit()
            message="Success"
        except Exception as ex:
            message=str(ex)
            return {"message": message, "banks": bank,"status":False}, 501
        finally:
            del(db_session)
        return {"message": message, "banks": bank,"status":True}, 201


    #Size
    def list(self,start,max,current_user):

        db_session = None
        banks=[]
        message=None
        size=0
        #bank=current_user.bank_id
        try:
            db_session = Connections().get_connection()
            bank = db_session.query(Banks).get(current_user.bank_id)
            #if bank:
            banks = db_session.query(Banks).all()
            if start == 0 and max == 0:
                pass
            elif start == 0 and max != 0:
                banks = banks[:max]
            elif start != 0 and max == 0:
                banks = banks[start:]
            elif start != 0 and max != 0:
                if start + max > start + max:
                    banks = banks[start:len(banks)]
                else:
                    banks = banks[start:start + max]
            else:
                pass

            message="Success"
            print(banks)
            if banks:
                size=len(banks)
            else:
                banks=[]
                size=0
            return {"message": message,
                    "banks": banks,
                    "start": start,
                    "max": max,
                    "size": size,
                    "status": True}, 201
        except Exception as ex:
            message=str(ex)
            return {"message": message,
                    "banks": banks,
                    "start": start,
                    "max": max,
                    "size":size,
                    "status":False}, 501
        finally:
            del(db_session)
