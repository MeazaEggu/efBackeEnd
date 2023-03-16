
from flask_restplus import Api, Resource, fields
from app import app
name_spacemy = app.namespace('names222', description='Manage names22')
@name_spacemy.route("/<int:id>")
class Test(Resource):
    def get(self):
        return {"fff0":21212}
        #@app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, params={ 'id': 'Specify the Id associated with the person' })
        #@app.doc(security='apikey')
        #@token_re
        #@usermanagament.login_required

