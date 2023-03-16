from flask_restplus import Api, Resource, fields
import json
class RequestImportDataFromFileDTO:
    def __init__(self):
        self.request = 'import_data_from_file', {'bank': fields.String(required = True, description="bank name", help="bank name")}
    def get_request(self):
        return self.request


class ResponsImportDataFromFileDTO:
    def __init__(self,json):
        self.status=""
        self._index=""
        self.result=""
        self.successful=""
        self._id=""
        self._seq_no=""
        self._version=""
        self._primary_term=""


    pass
    ##json respons =""


strr="{'_shards': {'total': 2, 'failed': 0, 'successful': 1}, '_type': 'testatm1', 'result': 'created', '_primary_term': 1, '_id': 'VwnW6XUBcx1gYcGC4tvX', '_index': 'testbank1', '_seq_no': 1319, '_version': 1}"
obj=ResponsImportDataFromFileDTO(json=json(strr))
obj.getR