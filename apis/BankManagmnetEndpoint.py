
from flask_restplus import Namespace, Resource, fields
from Services.UserManagmentServices import UserManagmentServices
from Services.BankManagmentServices import BankManagmentServices
#from apis.ATMManagmentEndpoint import atmRequestDTO
api = Namespace('banks', description='User managment')


bankRequestDTO = api.model('bankRequestDTO', {
    'name': fields.String( description='User username'),
})

bankDTO = api.model('bankDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
})

bankListResponseDTO=api.model('bankListResponseDTO', {
    'message': fields.String(description='message'),
    'banks':fields.List(fields.Nested(bankDTO)),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'status':fields.Boolean(description="descc")
})

bankResponseDTO=api.model('bankResponseDTO', {
    'message': fields.String(description='message'),
    'banks':fields.Nested(bankDTO),
    'status':fields.Boolean(description="descc")
})

paginationDTO=api.model('paginationDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

@api.route('/create')
class Create(Resource):
    @api.doc('Create Bank')
    @api.expect(bankRequestDTO)
    @api.marshal_with(bankResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        bankManagmentServices=BankManagmentServices(bankRequestDTO=api.payload)
        return bankManagmentServices.save(current_user=current_user)



@api.route('/list')
class List(Resource):
    @api.doc('List Banks')
    @api.expect(paginationDTO)
    @api.marshal_with(bankListResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss"])
    def post(current_user):
        return BankManagmentServices(bankRequestDTO=None).list(start=0,max=0,current_user=current_user)