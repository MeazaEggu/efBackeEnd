from flask_restplus import Namespace, Resource, fields
from Services.UserManagmentServices import UserManagmentServices
from Services.ATMManagmentServices import ATMManagmentServices

from apis.BankManagmnetEndpoint import bankRequestDTO, bankDTO
api = Namespace('ATMs', description='ATMs managment')

atmRequestDTO = api.model('atmRequestDTO', {
    #'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
    'bank': fields.Nested(bankDTO),
    #'bank_id': fields.Integer( description='band id'),
})

atmDTO = api.model('atmDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
    'bank': fields.Nested(bankDTO),
})

atmListResponseDTO=api.model('atmListResponseDTO', {
    'message': fields.String(description='message'),
    'atms':fields.List(fields.Nested(atmDTO)),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'status':fields.Boolean(description="desc")
})

atmResponseDTO=api.model('atmResponseDTO', {
    'message': fields.String(description='message'),
    'atms':fields.Nested(atmDTO),
    'status':fields.Boolean(description="desc")
})


atmsDTO = api.model('atmDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
})

banksDTO = api.model('bankDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
    'atm':fields.List(fields.Nested(atmsDTO),description="list")
})

allBanksAtmListResponseDTO=api.model('allBanksAtmListResponseDTO', {
    'message': fields.String(description='message'),
    'bank':fields.List(fields.Nested(banksDTO)),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'status':fields.Boolean(description="desc")
})

atmsByBankDTO = api.model('atmsByBankDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
    'bank_id': fields.Integer(description='User username'),
})

listATMsByBankResponseDTO=api.model('listATMsByBankResponseDTO',{
    'atms':fields.List(fields.Nested(atmsByBankDTO)),
    'message': fields.String(description='message'),
    'status':fields.Boolean(description="desc"),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

paginationDTO=api.model('paginationDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})

@api.route('/create')
class Create(Resource):
    @api.doc('Create atm')
    @api.expect(atmRequestDTO)
    @api.marshal_with(atmResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss"])
    def post(current_user):
        atmManagmentServices=ATMManagmentServices(atmRequestDTO=api.payload)
        return atmManagmentServices.save(current_user=current_user)


@api.route('/listAllBanksATms')
class List(Resource):
    @api.doc('listAllBanksATms')
    @api.expect(paginationDTO)
    @api.marshal_with(allBanksAtmListResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss"])
    def post(current_user):
        return ATMManagmentServices(atmRequestDTO=None).listAllBanksATms(start=api.payload["start"],max=api.payload["max"],current_user=current_user)

#For current user
@api.route('/listATMByBank')
class ListATMByBank(Resource):
    @api.doc('listATMByBank')
    @api.expect(paginationDTO)
    @api.marshal_with(listATMsByBankResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminbank","adminpss"])
    def post(current_user):
        return ATMManagmentServices(atmRequestDTO=None).listByBank(start=api.payload["start"],max=api.payload["max"],current_user=current_user)

listATMByBankIdDTO=api.model('listATMByBankIdDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'bank':fields.Nested(banksDTO)
})

listATMByBankIdResponseDTO=api.model('listATMByBankIdResponseDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'atms':fields.Nested(atmsDTO)
})

searchBanksDTO = api.model('searchBanksDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
})

searchAtmsDTO = api.model('searchAtmsDTO', {
    'id': fields.Integer( description='User id'),
    'name': fields.String( description='User username'),
    'bank_id': fields.Integer(description='User username'),
    'bank': fields.Nested(searchBanksDTO),
})
searchATMByNameResponseDTO=api.model('searchATMByNameResponseDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'atms':fields.List(fields.Nested(searchAtmsDTO))
})

@api.route('/listATMByBankId')
class ListATMByBankId(Resource):
    @api.doc('listATMByBankId')
    @api.expect(listATMByBankIdDTO)
    @api.marshal_with(listATMByBankIdResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss"])
    def post(current_user):
        return ATMManagmentServices(atmRequestDTO=None).listATMByBankId(payload=api.payload,current_user=current_user)



@api.route('/searchATMByName')
class searchATMByName(Resource):
    @api.doc('searchATMByName')
    @api.expect(searchAtmsDTO)
    @api.marshal_with(searchATMByNameResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","normalpss","adminbank","normalbank"])
    def post(current_user):
        return ATMManagmentServices(atmRequestDTO=None).searchATMByName(payload=api.payload,current_user=current_user)