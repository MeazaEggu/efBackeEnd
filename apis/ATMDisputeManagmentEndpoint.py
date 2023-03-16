from flask_restplus import Namespace, Resource, fields
from Services.UserManagmentServices import UserManagmentServices
from Services.ATMDisputeManagmentServices import ATMDisputeManagmentServices
from .BankManagmnetEndpoint import bankDTO
from .ATMManagmentEndpoint import atmDTO
from .UserManagmentEndpoint import userDTO
api = Namespace('atmdisputes', description='User managment')


atmDisputeDTO = api.model('atmDisputeDTO', {
    'id': fields.Integer( description='User username'),
    'amount': fields.Float( description='User username'),
    'dispute_at': fields.DateTime(description='User username'),
    'on_us': fields.Boolean(description='User username'),
    'off_us': fields.Boolean(description='User username'),
    'card_number': fields.String(description='User username'),
    'customer_name': fields.String(description='User username'),
    'bank': fields.Nested(bankDTO),
    'bank_name_dispute': fields.String(description='User username'),
    'atm': fields.Nested(atmDTO),
    'user':fields.Nested(userDTO),
    'userconfirmatmdispute':fields.Nested(userDTO),
    'bankdispute' : fields.Nested(bankDTO),
    'bank_name': fields.String(description='User username'),
    'atm_name': fields.String(description='User username'),
    'user_id': fields.Integer( description='User username'),
    'bank_id': fields.Integer( description='User username'),
    'bank_id_dispute': fields.Integer( description='User username'),
    'atm_id' : fields.Integer( description='User username'),
    'user_id_confirm_dispute' : fields.Integer( description='User username'),
    'confirm_status':fields.Boolean(),
})

atmDisputeRequestDTO = api.model('atmDisputeRequestDTO', {
    'amount': fields.Float( description='User username'),
    'dispute_at': fields.DateTime(description='User username'),
    'on_us': fields.Boolean(description='User username'),
    'off_us': fields.Boolean(description='User username'),
    'card_number': fields.String(description='User username'),
    'customer_name': fields.String(description='User username'),
    'bank': fields.Nested(bankDTO),
    'bank_name_dispute': fields.String(description='User username'),
    'atm': fields.Nested(atmDTO),
    'user':fields.Nested(userDTO),
    'bankdispute' : fields.Nested(bankDTO),
    'bank_name': fields.String(description='User username'),
    'atm_name': fields.String(description='User username'),
})


atmDisputeResponseDTO = api.model('responseAtmDisputeDTO', {
    'atmDispute': fields.Nested(atmDisputeDTO),
    'message': fields.String(description='User username'),
    'status': fields.Boolean(description='User username'),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

paginationDTO=api.model('paginationDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})


listATMDisputeDTO = api.model('listATMDisputeDTO', {
    'atmDisputes': fields.List(fields.Nested(atmDisputeDTO)),
    'message': fields.String(description='User username'),
    'status': fields.Boolean(description='User username'),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})


confirmATMDisputeResponseDTO = api.model('confirmATMDisputeResponseDTO', {
    'atmDispute': fields.Nested(atmDisputeDTO),
    'message': fields.String(description='User username'),
    'status': fields.Boolean(description='User username'),
})

@api.route('/createAtmDispute')
class Create(Resource):
    @api.doc('createAtmDispute')
    @api.expect(atmDisputeRequestDTO)
    @api.marshal_with(atmDisputeResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","normalbank"])
    def post(current_user):
        return ATMDisputeManagmentServices(atmDisputeRequestDTO=api.payload).createAtmDispute(current_user=current_user)


@api.route('/listAllATMDispute')
class ListAllATMDispute(Resource):
    @api.doc('listAllATMDispute')
    @api.expect(paginationDTO)
    @api.marshal_with(listATMDisputeDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss"])
    def post(current_user):
        return ATMDisputeManagmentServices(atmDisputeRequestDTO=None).listAllATMDispute(current_user=current_user,start=api.payload['start'],max=api.payload['max'])
        #return ATMManagmentServices(atmRequestDTO=None).listAllBanksATms(start=api.payload["start"],max=api.payload["max"],current_user=current_user)



@api.route('/confirmATMDispute')
class ConfirmATMDispute(Resource):
    @api.doc('confirmATMDispute')
    @api.expect(atmDisputeDTO)
    @api.marshal_with(confirmATMDisputeResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss"])
    def post(current_user):
        return ATMDisputeManagmentServices(atmDisputeRequestDTO=None).confirmATMDispute(payload=api.payload,current_user=current_user)#,start=api.payload['start'],max=api.payload['max'])
        #return ATMManagmentServices(atmRequestDTO=None).listAllBanksATms(start=api.payload["start"],max=api.payload["max"],current_user=current_user)

