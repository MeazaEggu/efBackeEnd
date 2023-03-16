from common.databases import Connections
from model.All import Users
from model.All import ATMs
from passlib.hash import sha256_crypt
import jwt
from functools import wraps
from flask import request
from model.All import Banks
class ATMManagmentServices:
    def __init__(self,atmRequestDTO):
        if atmRequestDTO!=None:
            self.atm = ATMs(
                name=atmRequestDTO['name'],
            )

            self.bank=Banks(
                id=atmRequestDTO['bank']["id"],
                #name=atmRequestDTO['bank']['name']
            )

    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJiYW5rIjoxLCJpZCI6MywidXNlcm5hbWUiOiJhd2FzaCIsInJvbGUiOiJiYW5rIn0.PszRacf9C4pzg18uWQZ3MlNh8SmzjZL7Cr0lel9wIFk
    def save(self,current_user):

        db_session = None
        message=None
        atm=None
        try:
            db_session = Connections().get_connection()
            bank = db_session.query(Banks).get(current_user.bank_id)
            if bank:
                checkAtmExistInTheBank=db_session.query(ATMs).filter(ATMs.bank_id==bank.id,ATMs.name==self.atm.name).count()
                if checkAtmExistInTheBank>=1:
                    message = "ATM name found in the bank"
                    return {"message": message, "atms": None, 'status': False}, 501
                else:
                    atm = self.atm
                    atm.id = None
                    atm.bank_id = bank.id
                    db_session.add(atm)
                    db_session.commit()
                    atm.bank=bank
                    message = "Success"
                    return {"message": message, "atms": atm, 'status': True}, 201
            else:
                message = "Bank not found"
                return {"message": message, "atms": None,'status':False}, 404

        except Exception as ex:
            if db_session:
                db_session.rollback()
            message=str(ex)
            return {"message": message, "atms": None,'status':False}, 501
        finally:
            del(db_session)


    #Size
    def listAllBanksATms(self, start, max, current_user):
        db_session = None
        atms = []
        message = None
        size = 0

        try:
            db_session = Connections().get_connection()
            if start == 0 and max == 0:
                atms = db_session.query(Banks).outerjoin(ATMs).group_by(Banks.id)
                banks = atms
            else:
                atms = db_session.query(ATMs).all()
            message = "Success"
            if atms:
                return {"message": message,
                        "bank": atms,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
            else:
                atms = []
                size = 0
        except Exception as ex:
            message = str(ex)
            return {"message": message,
                    "bank": atms,
                    "start": start,
                    "max": max,
                    "size": size,
                    'status':False}, 501
        finally:
            del (db_session)






    def listByBank(self,start,max,current_user):

        db_session = None
        atms=[]
        message=None
        size=0
        #bank=current_user.bank

        try:
            db_session = Connections().get_connection()
            bank = db_session.query(Banks).get(current_user.bank_id)#current_user.bank_id)
            if bank:
                atms = db_session.query(ATMs).filter(ATMs.bank_id == bank.id).all()
                if atms:
                    if start == 0 and max == 0:
                        pass
                    elif start == 0 and max != 0:
                        atms = atms[:max]
                    elif start != 0 and max == 0:
                        atms = atms[start:]
                    elif start != 0 and max != 0:
                        if start + max > start + max:
                            atms = atms[start:len(atms)]
                        else:
                            atms = atms[start:start + max]
                    else:
                        pass
                else:
                    message = "ATMs not found"
                    return {"message": message, "atms": None, 'status': False}, 404

                    # print(start,end,max)
                message = "Success"
                print(atms)
                if atms:
                    pass
                else:
                    atms = []
                    size = 0
                return {"message": message,
                        "atms": atms,
                        "start": start,
                        "max": max,
                        "size": len(atms),
                        'status': True}, 201
            else:
                message = "Bank not found"
                return {"message": message, "atms": None,'status':False}, 404
            #print(atms," size", size)
        except Exception as ex:
            message=str(ex)
            return {"message": message,
                    "atms": atms,
                    "start": start,
                    "max": max,
                    "size":size,
                    'status':False}, 501
        finally:
            del(db_session)


    def listATMByBankId(self,payload,current_user):

        db_session = None
        atms=[]
        message=None
        size=0
        #bank=current_user.bank
        bankId=payload['bank']['id']
        start=payload['start']
        max=payload['max']
        bank=None
        try:
            db_session = Connections().get_connection()
            bank = db_session.query(Banks).get(bankId)#current_user.bank_id)
            if bank:
                atms = db_session.query(ATMs).filter(ATMs.bank_id == bank.id).all()
                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    atms=atms[:max]
                elif start != 0 and max == 0:
                    atms=atms[start:]
                elif start != 0 and max != 0:

                    if start+max > start+max:
                        atms=atms[start:len(atms)]
                    else:
                        atms=atms[start:start+max]
                else:
                    pass
                message = "Success"
                if atms:
                    pass
                else:
                    atms = []
                    size = 0
                return {"message": message,
                        "atms": atms,
                        "start": start,
                        "max": max,
                        "size": len(atms),
                        'status': True}, 201
            else:
                message = "Bank not found"
                return {"message": message, "atms": None,'status':False}, 404
            #print(atms," size", size)
        except Exception as ex:
            #print("except")
            #print(ex)
            message=str(ex)
            return {"message": message,
                    "atms": None,
                    "start": start,
                    "max": max,
                    "size":size,
                    'status':False}, 501
        finally:
            del(db_session)

    def searchATMByName(self,payload,current_user):

        db_session = None
        atms=[]
        message=None
        size=0
        #bank=current_user.bank
        atmName=payload['name']
        bankId=0
        if payload['bank']['id']>0:
            bankId=payload['bank']['id']
        if payload['bank_id']>0:
            bankId = payload['bank_id']
        start=0#payload['start']
        max=0#payload['max']
        try:
            db_session = Connections().get_connection()
            if bankId>0:
                atms = db_session.query(ATMs).filter(ATMs.name == atmName).filter(ATMs.bank_id == bankId).all()
            else:
                atms = db_session.query(ATMs).filter(ATMs.name == atmName).all()
            if atms:
                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    atms=atms[:max]
                elif start != 0 and max == 0:
                    atms=atms[start:]
                elif start != 0 and max != 0:
                    if start+max > start+max:
                        atms=atms[start:len(atms)]
                    else:
                        atms=atms[start:start+max]
                else:
                    pass
                message = "Success"
                if atms:
                    pass
                else:
                    atms = []
                    size = 0
                return {"message": message,
                        "atms": atms,
                        "start": start,
                        "max": max,
                        "size": len(atms),
                        'status': True}, 201
            else:
                message = "Bank not found"
                return {"message": message, "atms": None,'status':False}, 404
            #print(atms," size", size)
        except Exception as ex:
            #print("except")
            #print(ex)
            message=str(ex)
            return {"message": message,
                    "atms": None,
                    "start": start,
                    "max": max,
                    "size":size,
                    'status':False}, 501
        finally:
            del(db_session)