from datetime import date
class Sources:
    SERVER_IP="http://localhost"
    PORT_NUMBER="9200"
    FTP_FILE_SOURCE = "file"
    DIRECTORY_TO_MOVE = "past"
    ELASTIC_SEACRH_URL=SERVER_IP+":"+PORT_NUMBER
    ELASTIC_SEACRH_URL_TYPE_NAME="atm"

    ELASTIC_SEACRH_URL_LIST_INDEX=SERVER_IP+":"+PORT_NUMBER+"/_cat/indices?format=json&pretty=true"
    ELASTIC_SEACRH_URL_LIST_DOCUMET=SERVER_IP+":"+PORT_NUMBER#+"/testindex/_search"

    #LOG_FILE_PATH="Log/mainlog.log"
    LOG_FILE_PATH = "Log/" + date.today().isoformat() + "_pss_ej_traker.log"
    def __init__(self):
        self.FILE_SOURCE="file"