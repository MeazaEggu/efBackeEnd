from flask_restplus import Api
from .UserManagmentEndpoint import api as ns3
from .EJManagmentEndpoint import api as ns4
from .ATMManagmentEndpoint import api as ns5
from .BankManagmnetEndpoint import api as ns6
from .PrivilageManagmentEndpoint import api as ns7
from .ATMDisputeManagmentEndpoint import api as ns8
authorizations = {
	'apikey':{
		'type':'apiKey',
		'in':'header',
		'name':'X-API-KEY'
	}
}
api = Api( title='PSS-EJ-Traker',
           version='1.0',
           description='EJ managment',
           authorizations=authorizations,
		   #prefix='/apis'
		   )
api.add_namespace(ns3,path="/apis/user")
api.add_namespace(ns4,path="/apis/ej")
api.add_namespace(ns5,path="/apis/atm")
api.add_namespace(ns6,path="/apis/bank")
api.add_namespace(ns7, path="/apis/privilage")
api.add_namespace(ns8, path="/apis/atmdispute")


