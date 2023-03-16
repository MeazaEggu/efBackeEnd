from flask_restplus import Namespace, Resource, fields
from Services.PrivilageManagmentServices import PrivilageManagmentServices
from Services.UserManagmentServices import UserManagmentServices
api = Namespace('Privilages', description='Privilages managment')

privilageDTO=api.model("privilageDTO",{
    'id': fields.Integer(required=True, description='User id'),
    'name': fields.String(required=True, description='User username'),
    'rolename': fields.String(required=True, description='User username'),
    'usertype': fields.String(required=True, description='User username'),
})

listPrivilageDTO=api.model("listPrivilageDTO",{
    'message': fields.String(required=True, description='User id'),
    'privilages': fields.List(fields.Nested(privilageDTO),required=True, description='User username'),
    'status':fields.Boolean(description="desc")
})


requestPrivilageDTO=api.model("requestPrivilageDTO",{
    'name': fields.String(required=True, description='User username'),
    'rolename': fields.String(required=True, description='User username'),
    'usertype': fields.String(required=True, description='User username'),
})
responsePrivilageDTO=api.model("responsePrivilageDTO",{
    'message': fields.String(required=True, description='User id'),
    'privilage': fields.Nested(privilageDTO,required=True, description='User username'),
    'status':fields.Boolean(description="desc")
})

paginationDTO=api.model('paginationDTO', {
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
})



@api.route('/create')
class Create(Resource):
    @api.doc('Create users')
    @api.expect(requestPrivilageDTO)
    @api.marshal_with(responsePrivilageDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        return PrivilageManagmentServices(privilageRequestDTO=api.payload).save()

@api.route('/list')
class List(Resource):
    @api.doc('listPrivilage')
    @api.expect(paginationDTO)
    @api.marshal_with(listPrivilageDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","adminbank"])
    def post(current_user):
        print(current_user.privilage.name)
        if current_user.privilage.name == "adminpss":
            return PrivilageManagmentServices(privilageRequestDTO=None).list(start=api.payload['start'],max=api.payload['max'])
        if current_user.privilage.name == "adminbank":
            return PrivilageManagmentServices(privilageRequestDTO=None).listByBank(start=api.payload['start'],max=api.payload['max'])



