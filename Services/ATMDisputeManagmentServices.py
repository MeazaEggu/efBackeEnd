from common.databases import Connections
from model.All import Users
from model.All import ATMs
from passlib.hash import sha256_crypt
import jwt
from functools import wraps
from flask import request
from model.All import Banks
from model.All import ATMDisputes
import datetime


class ATMDisputeManagmentServices:
    def __init__(self, atmDisputeRequestDTO):
        if atmDisputeRequestDTO != None:
            print(atmDisputeRequestDTO)
            # dateObject = datetime.datetime.strptime(atmDisputeRequestDTO['dispute_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            self.atmDispute = ATMDisputes(
                amount=atmDisputeRequestDTO['amount'],
                dispute_at=datetime.datetime.strptime(atmDisputeRequestDTO['dispute_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                on_us=atmDisputeRequestDTO['on_us'],
                off_us=atmDisputeRequestDTO['off_us'],
                card_number=atmDisputeRequestDTO['card_number'],
                bank_name=atmDisputeRequestDTO['bank_name'],
                bank_name_dispute=atmDisputeRequestDTO['bank_name_dispute'],
                atm_name=atmDisputeRequestDTO['atm_name'],
                customer_name=atmDisputeRequestDTO['customer_name'],
            )

            self.bank = Banks(
                id=atmDisputeRequestDTO['bank']["id"],
            )

            self.bankDispute = Banks(
                id=atmDisputeRequestDTO['bankdispute']["id"],
            )

            self.atm = ATMs(
                id=atmDisputeRequestDTO['atm']['id']
            )

    def createAtmDispute(self, current_user):

        db_session = None
        message = None
        atm = None
        bank = None
        bankDispute = None

        try:
            atmDispute = self.atmDispute
            print(atmDispute)
            db_session = Connections().get_connection()
            user = db_session.query(Users).get(current_user.id)
            bank = db_session.query(Banks).get(user.bank_id)
            bankDispute = db_session.query(Banks).get(self.bankDispute.id)
            atm = db_session.query(ATMs).get(self.atm.id)
            # TO CHECK IF ATM IS IN CURRENT USER BANK
            print(atm)
            print(bank)
            print(bankDispute)
            print(user)
            checkATMByATMIdAndBankID = None
            if atm:
                checkATMByATMIdAndBankID = db_session.query(ATMs).filter(ATMs.id == atm.id,
                                                                         ATMs.bank_id == bank.id).count()
            if bankDispute:
                atmDispute.bank_id_dispute = bankDispute.id
                atmDispute.bank_name_dispute = bankDispute.name
            else:
                pass

            if bank:
                atmDispute.bank_id = bank.id
                atmDispute.bank_name = bank.name
            else:
                pass
            # CHECK IF ATM IS IN CURRENT USER BANK
            if atm and checkATMByATMIdAndBankID >= 1:
                atmDispute.atm_id = atm.id
                atmDispute.atm_name = atm.name
            else:
                pass
            # Both on us and off-us can not be true and flase
            if atmDispute.on_us == True and atmDispute.off_us == True:
                message = "Both on-us and off-us can not be true"
                return {"message": message, "atmDispute": None, 'status': False, 'start': 0, 'max': 0, 'size': 0}, 501
            elif atmDispute.on_us == False and atmDispute.off_us == False:
                message = "Both on-us and off-us can not be false"
                return {"message": message, "atmDispute": None, 'status': False, 'start': 0, 'max': 0, 'size': 0}, 501
            else:
                pass

            if bank and user:
                '''atmDispute.atm=None
                atmDispute.bank=None
                atmDispute.bankdispute=None
                atmDispute.user=None'''
                if atmDispute.on_us == True:
                    atmDispute.bank_id_dispute = bank.id
                    atmDispute.bankdispute = bank

                atmDispute.user_id = user.id
                db_session.add(atmDispute)
                db_session.commit()
                message = "Success"
                return {"message": message, "atmDispute": atmDispute, 'status': True, 'start': 0, 'max': 0,
                        'size': 0}, 201
            else:
                message = "Bank not found"
                return {"message": message, "atmDispute": None, 'status': False, 'start': 0, 'max': 0, 'size': 0}, 404

        except Exception as ex:
            if db_session:
                db_session.rollback()
            message = str(ex)
            return {"message": message, "atmDispute": None, 'status': False, 'start': 0, 'max': 0, 'size': 0}, 501
        finally:
            del (db_session)

    # Size
    def listAllATMDispute(self, start, max, current_user):
        db_session = None
        atmDisputes = []
        message = None
        size = 0
        try:
            db_session = Connections().get_connection()
            # atmDisputes = db_session.query(ATMDisputes).outerjoin(Banks).group_by(Banks.id)
            # atmDisputes = ATMDisputes.join(Banks, Banks.id == ATMDisputes.bank_id).group_by(Banks.id)
            # query.join(Customer.invoices)
            atmDisputes = db_session.query(ATMDisputes).all()  # join(Banks.atmdispute).group_by(Banks.id)
            if start == 0 and max == 0:
                pass
            elif start == 0 and max != 0:
                atmDisputes = atmDisputes[:max]
            elif start != 0 and max == 0:
                atmDisputes = atmDisputes[start:]
            elif start != 0 and max != 0:

                if start + max > start + max:
                    atmDisputes = atmDisputes[start:len(atmDisputes)]
                else:
                    atmDisputes = atmDisputes[start:start + max]
            else:
                pass
            size = len(atmDisputes)

            message = "Success"
            if atmDisputes:
                return {"message": message,
                        "atmDisputes": atmDisputes,
                        "start": start,
                        "max": max,
                        "size": size,
                        'status': True}, 201
            else:
                atmDisputes = []
                size = 0
        except Exception as ex:
            message = str(ex)
            return {"message": message,
                    "atmDisputes": atmDisputes,
                    "start": start,
                    "max": max,
                    "size": size,
                    'status': False}, 501
        finally:
            del (db_session)

    def confirmATMDispute(self, payload, current_user):
        db_session = None
        atms = []
        message = None
        atmDispute = None
        try:
            atmDisputeId = payload['id']
            db_session = Connections().get_connection()
            user = db_session.query(Users).get(current_user.id)
            if atmDisputeId != None and atmDisputeId != 0 and user != None:
                atmDispute = db_session.query(ATMDisputes).get(atmDisputeId)
                if atmDispute:
                    if atmDispute.off_us == True and atmDispute.on_us == False:
                        if user.privilage.usertype == "pss":
                            atmDispute.confirm_status = True
                            atmDispute.user_id_confirm_dispute = user.id
                            atmDispute.userconfirmatmdispute = user
                            db_session.commit()
                            message = "Success"
                            return {"message": message, "atmDispute": atmDispute, 'status': True}, 201
                        else:
                            message = "You have not enough privilage"
                            return {"message": message, "atmDispute": atmDispute, 'status': False}, 401
                    elif atmDispute.off_us == False and atmDispute.on_us == True:
                        if user.privilage.usertype == "bank":
                            if user.bank_id == atmDispute.bank_id:
                                atmDispute.confirm_status = True
                                atmDispute.user_id_confirm_dispute = user.id
                                atmDispute.userconfirmatmdispute = user
                                db_session.commit()
                                message = "Success"
                                return {"message": message, "atmDispute": atmDispute, 'status': True}, 201
                            else:
                                message = "You have not enough privilage"
                                return {"message": message, "atmDispute": atmDispute, 'status': False}, 401
                        else:
                            message = "You have not enough privilage"
                            return {"message": message, "atmDispute": atmDispute, 'status': False}, 401
                    else:
                        message = "You have not enough privilage"
                        return {"message": message, "atmDispute": atmDispute, 'status': False}, 401
                else:
                    message = "ATM dispute can not be found"
                    return {"message": message, "atmDispute": atmDispute, 'status': False}, 404
            else:
                message = "ATM dispute can not be found"
                return {"message": message, "atmDispute": atmDispute, 'status': False}, 404
        except Exception as ex:
            message = str(ex)
            print(ex)
            return {"message": message, "atmDispute": None, 'status': False}, 501
        finally:
            del (db_session)
