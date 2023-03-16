from common.databases import Connections
from model.All import *
from passlib.hash import sha256_crypt
import jwt
from functools import wraps
from flask import request

class UserManagmentServices:
    def __init__(self,userRequestDTO):
        if userRequestDTO!=None:

            self.bank = Banks(
                id=userRequestDTO['bank']["id"],
                name=userRequestDTO['bank']["name"]
            )

            self.privilage=Privilages(
                id= userRequestDTO['privilage']['id'],
                name= userRequestDTO['privilage']['name'],
                rolename= userRequestDTO['privilage']['rolename'],
                usertype= userRequestDTO['privilage']['usertype'],
            )
            self.user = Users(
                username=userRequestDTO['username'],
                firstname=userRequestDTO['firstname'],
                middlename=userRequestDTO['middlename'],
                lastname=userRequestDTO['lastname'],
                password=sha256_crypt.encrypt(userRequestDTO['password']),
                email=userRequestDTO['email'],
                privilage_id=self.privilage.id,
                bank_id=self.bank.id
            )

    def save(self):
        db_session = None
        message=None
        user=None
        bank = None
        privilage = None
        db_session=None
        try:
            db_session = Connections().get_connection()
            user=self.user
            checkUserNameNotUsed = db_session.query(Users).filter_by(username=self.user.username).count()
            if checkUserNameNotUsed >= 1:
                message = "User name can not be used"
                return {"message": message, "user": None, 'status': False}, 501

            if self.bank.id!=None and self.bank.id!=0:
                bank=db_session.query(Banks).get(self.bank.id)
                if bank==None:
                    message = "Bank not found"
                    return {"message": message, "user": None, 'status': False}, 501
                else:
                    user.bank_id=bank.id
            else:
                user.bank_id=None

            if self.privilage.id!=None and self.privilage.id!=0:
                privilage=db_session.query(Privilages).get(self.privilage.id)
                if privilage==None:
                    message = "Privilage not found"
                    return {"message": message, "user": None, 'status': False}, 404
                else:
                    user.privilage_id = privilage.id
                    #if current usr is bank create user for bank else pss user can create for it self or any
            else:
                message = "Privilage not found"
                return {"message": message, "user": None, 'status': False}, 404

            db_session.add(user)
            db_session.commit()
            message="Success"
            return {"message": message, "user": user, 'status': True}, 201
        except Exception as ex:
            if db_session:
                db_session.rollback()
            message=str(ex)
            return {"message": message, "user": user,'status':False}, 501
        finally:
           del(db_session)



    def saveByBank(self,current_user):
        db_session = None
        message = None
        user = None
        bank = None
        privilage = None
        db_session = None
        try:
            db_session = Connections().get_connection()
            user = self.user
            checkUserNameNotUsed = db_session.query(Users).filter_by(username=self.user.username).count()
            if checkUserNameNotUsed >= 1:
                message = "User name can not be used"
                return {"message": message, "user": None, 'status': False}, 501

            bank = db_session.query(Banks).get(current_user.bank_id)
            if bank:
                user.bank_id=bank.id
            else:
                message = "Bank not found"
                return {"message": message, "user": None, 'status': False}, 501

            if self.privilage.id!=None and self.privilage.id!=0:
                privilage=db_session.query(Privilages).get(self.privilage.id)
                if privilage==None:
                    message = "Privilage not found"
                    return {"message": message, "user": None, 'status': False}, 404
                else:
                    #CHeck if the privilage is for bank user
                    if privilage.usertype=="bank":
                        user.privilage_id = privilage.id
                    else:
                        message = "User with this privilage can not be created"
                        return {"message": message, "user": None, 'status': False}, 401

            else:
                message = "Privilage not found"
                return {"message": message, "user": None, 'status': False}, 404

            db_session.add(user)
            db_session.commit()
            message = "Success"
            return {"message": message, "user": user, 'status': True}, 201

        except Exception as ex:
            if db_session:
                db_session.rollback()
            message = str(ex)
            return {"message": message, "user": user, 'status': False}, 501

        finally:
            del (db_session)


    #Size
    def list(self,start,max):
        db_session = None
        users=None
        message=None
        size=0
        try:

            db_session = Connections().get_connection()
            users = db_session.query(Users).all()
            if users:
                if start == 0 and max == 0:
                    pass
                elif start == 0 and max != 0:
                    users=users[:max]
                elif start != 0 and max == 0:
                    users=users[start:]
                elif start != 0 and max != 0:
                    if start + max > start + max:
                        users = users[start:len(users)]
                    else:
                        users = users[start:start + max]
                else:
                    pass
                message="Success"
                if users:
                    size=len(users)

                return {"message": message,
                        "user": users,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
            else:
                message="No user found"
                return {"message": message,
                        "user": users,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
        except Exception as ex:
            message=str(ex)
            return {"message": message,
                    "user": None,
                    "start": start,
                    "max": max,
                    "size":size,
                    'status':False}, 501
        finally:
            del(db_session)

    def listAllPrivilages(self,current_user):
        db_session = None
        privilages=None
        try:
            db_session = Connections().get_connection()
            privilages = db_session.query(Privilages).all()
            return {"message":"success", "privilages": privilages, 'status': True}, 201
        except Exception as ex:
            return {"message": str(ex), "privilages": privilages, 'status': False}, 501
        finally:
            del (db_session)



    def login(self,username,password):
        db_session=None
        try:
            message=None
            if username!=None and username!="" and password!=None and password!="":
                user=None
                db_session = Connections().get_connection()
                user_count=db_session.query(Users).filter_by(username=username).count()
                if user_count:
                    user=db_session.query(Users).join(Privilages).filter(Users.username==username).first()
                    print(user.username)
                    #user = db_session.query(Users).filter_by(username=username).first()
                    authrnticate=sha256_crypt.verify(password, str(user.password))
                    if authrnticate:
                        token=jwt.encode({'id':user.id,'username': user.username, 'bank':user.bank_id,'privilage':user.privilage_id}, 'secret', algorithm='HS256')
                        return {"message":"success","token": token.decode(),'privilage':user.privilage,'status':True}, 201
                    else:
                        return {"message": "username or password is incorrect", "token": None, "privilage": None,
                                'status': False}, 401
                else:
                    return {"message": "username or password is incorrect","token": None,"privilage":None,'status':False}, 401
            else:
                return {"message":"Invalid username and password","token": None,"privilage":None,'status':False},401
        except Exception as ex:
            return {"message": str(ex),"token": None,"privilage":None,'status':False}, 501
        finally:
            del(db_session)

    @staticmethod
    def privilage(privilage_name):
        #print(privilage_name)
        def rolechecker(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                user = None
                token = None
                if 'X-API-KEY' in request.headers:
                    token = request.headers['X-API-KEY']
                if not token:
                    return {'message': 'token is messing','status':False}, 401
                try:
                    user_data = jwt.decode(token, 'secret', algorithms=['HS256'])
                    db_session = Connections().get_connection()
                    print(user_data["username"])
                    user_featched = db_session.query(Users).join(Privilages).filter(Users.username==user_data['username'])
                    if user_featched:
                        user=user_featched.first()
                        kwargs["user"]=user
                        print("pppp")
                        print(privilage_name)
                        print(user.privilage.name)
                        print(user.username)
                        if user.privilage.name in privilage_name:
                            pass
                        else:
                            return {'message': 'invalid token','status':False}, 401
                    else:
                        return {'message': 'invalid token','status':False}, 401
                except Exception as ex:
                    return {'message': str(ex),'status':False}, 401
                return func(user)
            return wrapped_function

        return rolechecker