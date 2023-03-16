
from flask_restplus import Namespace, Resource, fields
from Services.UserManagmentServices import UserManagmentServices
from Services.EJManagmentServices import EJManagmentServices
from apis.BankManagmnetEndpoint import bankDTO
from apis.ATMManagmentEndpoint import atmsDTO
api = Namespace('EJs', description='EJ managment')


ejDTO = api.model('ejDTO', {
    'id': fields.String(required=True, description='User id'),
    'bank': fields.String(required=True, description='User username'),
    'transaction_type':fields.String(required=True, description='User password'),
    'response_code': fields.String(required=True, description='User bank name'),
    'response_message': fields.String( description='User bank name'),
    'end_transaction_date_time': fields.String(required=True, description='User bank name'),
    'start_transaction_date_time': fields.String(required=True, description='User bank name'),
    'response_status': fields.Integer(required=True, description='User bank name'),
    'sequence_number': fields.String(required=True, description='User bank name'),
    'auth_number': fields.String(required=True, description='User bank name'),
    'users_bank': fields.String(required=True, description='User bank name'),
    'atm': fields.String(required=True, description='User bank name'),
    'atm_type': fields.String(required=True, description='User bank name'),
    'amount': fields.String(required=True, description='User bank name'),
    'card_number': fields.String(required=True, description='User bank name'),
    'detail': fields.String(required=True, description='User bank name'),
})

ejResponseDTO=api.model("ejResponseDTO",{
    '_index': fields.String(description='message'),
    '_type': fields.String(description='message'),
    '_id': fields.String(description='message'),
    '_source':fields.Nested(ejDTO,"EJ"),
    '_score':fields.Float(description='message')
})

ejResponseListDTO=api.model('ejResponseListDTO',{
    'ejs': fields.List(fields.Nested(ejResponseDTO)),
    'message':fields.String(description='message')
})


listEJResponseDTO=api.model('listEJResponseDTO', {
    'message': fields.String(description='message'),
    'ej':fields.List(fields.Nested(ejDTO)),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

requestEJBYATMDTO=api.model("requestEJBYATMDTO",{
    #'id':fields.Integer(required=True, description='atm'),
    #'name':fields.String(required=True, description='atm'),
    "atm":fields.Nested(atmsDTO,"desc"),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

fillterEJByATMRequestDTO=api.model('fillterEJByATMRequestDTO', {
    'atm': fields.String(required=True,description='atm'),
})



paginationDTO=api.model('paginationDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})


requestEJBYBankIdAndATMIdDTO=api.model("requestEJBYBankIdAndATMIdDTO",{
    "atm":fields.Nested(atmsDTO,"desc"),
    "bank":fields.Nested(bankDTO,"desc"),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),

})

@api.route('/list')
#@api.response(404, 'User not found')
class List(Resource):
    @api.doc('List EJ')
    @api.expect(paginationDTO)
    @api.marshal_with(listEJResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    #@api.route('/api/rec/<string:uid>')
    #@UserManagmentServices.login_required
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        #return UserManagmentServices(userRequestDTO=None).list(api.payload['start'],api.payload['end'],api.payload['max'])

@api.route('/listEJByATMId')
class listEJByATMId(Resource):
    @api.doc('listEJByATMId')
    #@api.marshal_with(ejResponseListDTO, code=201, description='Success with response data')
    @api.expect(requestEJBYATMDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss","normalpss","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().listEJByATMId(atmpyload=api.payload,current_user=current_user)


@api.route('/listEJByBankIdAndATMId')
class listEJByBankIdAndATMId(Resource):
    @api.doc('listEJByBankIdAndATMId')
    #@api.marshal_with(ejResponseListDTO, code=201, description='Success with response data')
    @api.expect(requestEJBYBankIdAndATMIdDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().listEJByBankIdAndATMId(payload=api.payload,current_user=current_user)



requestGetCountTransactionByATMIdDTO=api.model("requestGetCountTransactionSuccessByATMIdDTO",{
    "atm":fields.Nested(atmsDTO,"desc"),
})

requestGetCountTransactionByBanksIdDTO=api.model("requestGetCountTransactionSuccessByBanksIdDTO",{
    "bank":fields.Nested(bankDTO,"desc"),
})

responseGetCountTransactionDTO=api.model('responseGetCountTransactionSuccessByATMIdDTO',{
    'count': fields.Integer(description='count'),
    'message':fields.String(description='message'),
    "status":fields.Boolean(description="desc")
})

@api.route('/getCountTransactionSuccessByATMId')
class getCountTransactionSuccessByATMId(Resource):
    @api.doc('getCountTransactionSuccessByATMId')
    @api.marshal_with(responseGetCountTransactionDTO, code=201, description='Success with response data')
    @api.expect(requestGetCountTransactionByATMIdDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss","normalpss","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().getCountTransactionSuccessByATMId(payload=api.payload,current_user=current_user)

@api.route('/getCountTransactionFailedByATMId')
class getCountTransactionFailedByATMId(Resource):
    @api.doc('getCountTransactionFailedByATMId')
    @api.marshal_with(responseGetCountTransactionDTO, code=201, description='Success with response data')
    @api.expect(requestGetCountTransactionByATMIdDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss","normalpss","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().getCountTransactionFailedByATMId(payload=api.payload,current_user=current_user)



@api.route('/getCountTransactionSuccessByBankId')
class getCountTransactionSuccessByBankId(Resource):
    @api.doc('getCountTransactionSuccessByBankId')
    @api.marshal_with(responseGetCountTransactionDTO, code=201, description='Success with response data')
    @api.expect(requestGetCountTransactionByBanksIdDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss","normalpss","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().getCountTransactionSuccessByBankId(payload=api.payload,current_user=current_user)

@api.route('/getCountTransactionFailedByBankId')
class getCountTransactionFailedByBankId(Resource):
    @api.doc('getCountTransactionFailedByBankId')
    @api.marshal_with(responseGetCountTransactionDTO, code=201, description='Success with response data')
    @api.expect(requestGetCountTransactionByBanksIdDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss","normalpss","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().getCountTransactionFailedByBankId(payload=api.payload,current_user=current_user)



"""requestFillterDTO=api.model("requestFillterDTO",{
    "bank":fields.Nested(bankDTO,"desc"),
})
"""
requestFillterDTO=api.model('requestFillterDTO',{
    "bank":fields.Nested(bankDTO,description='message'),
    "response_code":fields.String(description="desc"),
    "response_status": fields.Integer(description="desc"),
    "users_bank": fields.String(description="desc"),
    "atm": fields.Nested(atmsDTO,description="desc"),
    "atm_type": fields.String(description="desc"),
    "start":fields.Integer(description=""),
    "max": fields.Integer(description=""),
    "size":fields.Integer(description=""),
})

@api.route('/fillterByBankId')
class fillterByBankId(Resource):
    @api.doc('fillterByBankId')
    #@api.marshal_with(responseGetCountTransactionDTO, code=201, description='Success with response data')
    @api.expect(requestFillterDTO)
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss","adminbank","normalbank"])
    def post(current_user):
        print(current_user)
        print(api.payload)
        return EJManagmentServices().fillterByBankId(payload=api.payload, current_user=current_user)


