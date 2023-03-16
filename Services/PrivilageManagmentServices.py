from common.databases import Connections
from model.All import *
from passlib.hash import sha256_crypt
import jwt
from functools import wraps
from flask import request

class PrivilageManagmentServices:
    def __init__(self,privilageRequestDTO):
        if privilageRequestDTO!=None:
            self.privilage = Privilages(
                name=privilageRequestDTO["name"],
                rolename=privilageRequestDTO["rolename"],
                usertype=privilageRequestDTO["usertype"]
            )
    def save(self):
        db_session = None
        message=None
        privilage = None
        db_session=None
        try:
            db_session = Connections().get_connection()
            privilage=self.privilage
            checkNameNotUsed = db_session.query(Privilages).filter_by(name=self.privilage.name).count()
            if checkNameNotUsed >= 1 :
                message = "Privilages name can not be used"
                return {"message": message, "privilage": None, 'status': False}, 501

            db_session.add(privilage)
            db_session.commit()
            message="Success"
            return {"message": message, "privilage": privilage, 'status': True}, 201

        except Exception as ex:
            if db_session:
                db_session.rollback()
            message=str(ex)
            return {"message": message, "privilage": privilage,'status':False}, 501
        finally:
           del(db_session)


    #Size
    def list(self,start,max):
        db_session = None
        privilages=None
        message=None
        size=0
        try:
            db_session = Connections().get_connection()
            privilages = db_session.query(Privilages).all()
            if privilages:
                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    privilages=privilages[:max]
                elif start != 0 and max == 0:
                    privilages=privilages[start:]
                elif start != 0 and max != 0:
                    if start + max > start + max:
                        privilages = privilages[start:len(privilages)]
                    else:
                        privilages = privilages[start:start + max]
                else:
                    pass
                message="Success"
                if privilages:
                    size=len(privilages)
                return {"message": message,
                        "privilages": privilages,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
            else:
                message="No privilage found"
                return {"message": message,
                        "privilages": privilages,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
        except Exception as ex:
            message=str(ex)
            return {"message": message,
                    "privilages": privilages,
                    "start": start,
                    "max": max,
                    "size":size,
                    'status':False}, 501
        finally:
            del(db_session)



    def listByBank(self,start,max):
        db_session = None
        privilages = None
        message = None
        size = 0
        try:
            db_session = Connections().get_connection()
            privilages = db_session.query(Privilages).filter(Privilages.usertype=="bank").all()
            if privilages:
                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    privilages = privilages[:max]
                elif start != 0 and max == 0:
                    privilages = privilages[start:]
                elif start != 0 and max != 0:
                    if start + max > start + max:
                        privilages = privilages[start:len(privilages)]
                    else:
                        privilages = privilages[start:start + max]
                else:
                    pass
                message = "Success"
                if privilages:
                    size = len(privilages)
                return {"message": message,
                        "privilages": privilages,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
            else:
                message = "No privilage found"
                return {"message": message,
                        "privilages": privilages,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
        except Exception as ex:
            message = str(ex)
            return {"message": message,
                    "privilages": privilages,
                    "start": start,
                    "max": max,
                    "size": size,
                    'status': False}, 501
        finally:
            del (db_session)
