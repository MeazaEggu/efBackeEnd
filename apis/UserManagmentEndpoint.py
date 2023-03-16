from flask_restplus import Namespace, Resource, fields
from Services.UserManagmentServices import UserManagmentServices
api = Namespace('Users', description='User managment')

from apis.BankManagmnetEndpoint import bankDTO
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

userRequestDTO = api.model('userRequestDTO', {
    'username': fields.String(required=True, description='User username'),
    'password':fields.String(required=True, description='User password'),
    'bank': fields.Nested(bankDTO,required=True, description='User bank'),
    'privilage': fields.Nested(privilageDTO, required=True, description='User bank'),#fields.String(required=True, description='User bank name'),
    'firstname': fields.String(required=True, description='User bank name'),
    'middlename': fields.String(required=True, description='User bank name'),
    'lastname': fields.String(required=True, description='User bank name'),
    'email': fields.String(required=True, description='User bank name'),
})

userResponseDTO = api.model('UserResponse', {
    'id': fields.String(required=True, description='User id'),
    'username': fields.String(required=True, description='User username'),
    'bank': fields.Nested(bankDTO,required=True, description='User bank'),
    'privilage': fields.Nested(privilageDTO, required=True, description='User bank'),
    'firstname': fields.String(required=True, description='User bank name'),
    'middlename': fields.String(required=True, description='User bank name'),
    'lastname': fields.String(required=True, description='User bank name'),
    'email': fields.String(required=True, description='User bank name'),
})


createUserResponseDTO=api.model('createUserResponseDTO', {
    'message': fields.String(description='message'),
    'user':fields.Nested(userResponseDTO),
    'status':fields.Boolean(description="desc")
})

userDTO=api.model('userDTO', {
    'id': fields.String(required=True, description='User id'),
    'bank': fields.Nested(bankDTO,required=True, description='User bank'),
    'privilage': fields.Nested(privilageDTO, required=True, description='User bank'),
    'firstname': fields.String(required=True, description='User bank name'),
    'middlename': fields.String(required=True, description='User bank name'),
    'lastname': fields.String(required=True, description='User bank name'),
    'email': fields.String(required=True, description='User bank name'),
})

listUserDTO=api.model('listUserDTO', {
    'message': fields.String(description='message'),
    'user':fields.List(fields.Nested(userResponseDTO)),
    'start': fields.Integer(required=True, description='User id'),
    'max':fields.Integer(required=True, description='User password'),
    'size':fields.Integer(description='User password'),
    'status':fields.Boolean(description="desc")
})


loginUserDTO=api.model('loginUserDTO', {
    'username': fields.String(required=True,description='message'),
    'password': fields.String(required=True, description='Password'),
    'token': fields.String( description='Token'),
    'message':fields.String( description='Message'),
    'privilage': fields.Nested(privilageDTO, required=True, description='User bank'),
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
    @api.expect(userRequestDTO)
    @api.marshal_with(createUserResponseDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss","adminbank"])
    def post(current_user):
        if current_user.privilage.name == "adminpss":
            return UserManagmentServices(userRequestDTO=api.payload).save()
        if current_user.privilage.name == "adminbank":
            return UserManagmentServices(userRequestDTO=api.payload).saveByBank(current_user=current_user)

@api.route('/list')
class List(Resource):
    @api.doc('List users')
    @api.expect(paginationDTO)
    @api.marshal_with(listUserDTO, code=201, description='Success with response data')
    @api.doc(security='apikey')
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        return UserManagmentServices(userRequestDTO=None).list(start=api.payload['start'],max=api.payload['max'])

@api.route('/login')
class Login(Resource):
    @api.doc('Login users')
    @api.expect(loginUserDTO)
    @api.marshal_with(loginUserDTO, code=201, description='Success with response data')
    def post(self):
        return UserManagmentServices(userRequestDTO=None).login(username=api.payload["username"],password=api.payload["password"])#api.payload['start'],api.payload['end'],api.payload['max'])

"""@api.route('/listAllPrivilages')
class ListAllPrivilages(Resource):
    @api.doc('Login users')
    #@api.expect(loginUserDTO)
    @api.marshal_with(listPrivilageDTO, code=201, description='Success with response data')
    @UserManagmentServices.privilage(["adminpss"])
    def post(current_user):
        return UserManagmentServices(userRequestDTO=None).listAllPrivilages(current_user=current_user)"""