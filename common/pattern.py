class Patterns:
    NCR_ATM_LOG_FILE_SINGLE_TRANSACTION_PATTERN = r"TRANSACTION START((?!(TRANSACTION START))[^'])*TRANSACTION END"
    """TRANSACTION\s{1}START[^']*TRANSACTION\s{1}END"""
    #DIEBOLD_ATM_LOG_FILE_SINGLE_TRANSACTION_PATTERN= r"(Card Inserted((?!(----------------------------------------------))[^'])*----------------------------------------------)"
    DIEBOLD_ATM_LOG_FILE_SINGLE_TRANSACTION_PATTERN=r"\d{8}\s{1}\d{4}\s{1}\d{2}\/{1}\d{2}\/{1}\d{4}\s{1}\d{2}\:\d{2}\:\d{2}\s{1}(Card Inserted((?!(----------------------------------------------))[^'])*----------------------------------------------)"
    DIEBOLD_ATM_SPLIT_ROW_START_INDEX=1

    #DIEBOLD_ATM_LOG_PATTERN="\d{8}\s\d{4}\s\d{2}\/\d{2}\/\d{4}\s\d{2}\:\d{2}\:\d{2}\s----------------------------------------------\n\d{8}\s\d{4}\s\d{2}\/\d{2}\/\d{4}\s\d{2}\:\d{2}\:\d{2}\sCard Inserted.*\n"
    #NCR_ATM_LOG_PATTERN="(.*\n)*TRANSACTION START"
    NCR_ATM_LOG_FILE_NAME_PATTERN=r"\d{4}-\d{2}-\d{2}_[a-zA-Z0-9]{3,}_EJDATA.log"
    DIEBOLD_ATM_LOG_FILE_NAME_PATTERN=r"EJMyTerminalID[.]\d{4}\d{2}\d{2}(_TO_\d{4}\d{2}\d{2})*[.]\d{6}"

    NCR_ATM_LOG_SPLIT_TRANSACTION_PATTERN="TRANSACTION START"
    DIEBOLD_ATM_LOG_SPLIT_TRANSACTION_PATTERN="----------------------------------------------"

    INDEX_NAME_PATTERN=r"^[a-zA-Z0-9]*$"#r'^[BANK][a-zA-Z0-9]*$'
    TEMP_INDEX_NAME_PATTERN=r"[a-zA-Z]*[0-9]{0,1}\_temp"

    NCR_ATM_LOG_LINE_SEQUENCE_NUMBER_PATTERN=r"\(\d{2,3}[\/]\d{2,3}[\/]\d{2,3}\s{1}\(\d{2,3}\:\d{2,3}\:\d{2,3}\s{1}\(\d{5,6}"
    NCR_ATM_LOG_SEQUENCE_NUMBER_PATTERN=r"\d{5,6}"
    DIEBOLD_ATM_LOG_LINE_SEQUENCE_NUMBER_PATTERN=r"\d{8}\s{1}\d{4}\s{1}\d{2}\/{1}\d{2}\/{1}\d{4}\s{1}\d{2}\:\d{2}\:\d{2}\s{1}Transaction Reply \[Host Seq.No.:\s{1}\d{4,6}\]"
    DIEBOLD_ATM_LOG_SEQUENCE_NUMBER_PATTERN=r"\[Host Seq.No.:\s{1}\d{4,6}\]"

    NCR_ATM_LOG_CARD_NUMBER="\(\d{1,2}[a-zA-Z]*\s{1}[a-zA-Z]*\s{1}:\s{1}\(\d{7,9}[X]{6,7}\d{4,6}"
    DIEBOLD_ATM_LOG_CARD_NUMBER="\d{8}\s{1}\d{4}\s{1}\d{2}\/{1}\d{2}\/{1}\d{4}\s{1}\d{2}\:\d{2}\:\d{2}\s{1}Card Inserted\s{1}\(\d{4,6}\s{1}\d{2,3}[X]{2,3}\s{1}[X]{4}\s{1}\d{4}"

    NCR_ATM_LOG_TRANSACTION_AMOUNT_PATTERN=r"\(\d{1}AMOUNT\s{1}:\s{1}\(\d*\s{1}\(\d{1}ETB"
    DIEBOLD_ATM_LOG_TRANSACTION_AMOUNT_PATTERN=r"AMOUNT\s{1}:\d*ETB"

    #NCR_ATM_LOG_TRANSACTION_RESPONSE_PATTERN=r"\(\d{1}RESPONSE\s{1}:\s{1}\(\d{1,2}\s{1}\d{1,2}\w+\s{1}\w+(\s\w+)+"
    NCR_ATM_LOG_TRANSACTION_RESPONSE_PATTERN=r"\(\d{1}RESPONSE\s{1}:\s{1}\(\d{1,2}\s{1}\d{1,2}\w*\s{1}((\w*)|\s{1})*\w"
    #NCR_ATM_LOG_TRANSACTION_RESPONSE_PATTERN=r"\(\d{1}RESPONSE\s{1}:\s{1}\(\d{1,2}\s{1}\d{1,2}(\w*\s{0,1})*"
    DIEBOLD_ATM_LOG_TRANSACTION_RESPONSE_PATTERN=r"RESPONSE\s{1}:\d{1,2}\s{1}\d{2}\w+(\s{1}\w+)*"

    NCR_ATM_LOG_TRANSACTION_RESPONSE_SUCCESS_PATTERN=r"\(1RESPONSE\s{1}:\s{1}\(\d{1,3}\s{1}\d{1,3}APPROVED OR COMPLETED SUCCESSFULLY"
    DIEBOLD_ATM_LOG_TRANSACTION_RESPONSE_SUCCESS_PATTERN=r"RESPONSE :\d{1,2} \d{1,3}APPROVED OR COMPLETED SUCCESSFULLY"

    NCR_ATM_LOG_TRANSACTION_AUTH_NUMB_PATTERN=r"\(\d{1}AUTH NUMB:\s{1}\(\d{1,8}"
    DIEBOLD_ATM_LOG_TRANSACTION_AUTH_NUMB_PATTERN=r"AUTH NUMB:\d{0,8}"

    NCR_ATM_LOG_TRANSACTION_NOTES_PRESENTED_PATTERN=r"(NOTES PRESENTED)|(NOTES TAKEN)"
    DIEBOLD_ATM_LOG_TRANSACTION_NOTES_PRESENTED_PATTERN=r"(Cash Present)|(Present)|(Cash Taken)"

    NCR_ATM_LOG_TRANSACTION_ACCOUNT_PATTERN=r"\(\d{1}ACCOUNT:\s{1}\(\d{0,10}"
    DIEBOLD_ATM_LOG_TRANSACTION_ACCOUNT_PATTERN = r"ACCOUNT:\d{0,10}"

    NCR_ATM_LOG_TRANSACTION_TYPE_PATTERN=r"(BALANCE INQUIRY)|(CASH WITHDRAWAL)"
    DIEBOLD_ATM_LOG_TRANSACTION_TYPE_PATTERN=r"(BALANCE INQUIRY)|(CASH WITHDRAWAL)"

    NCR_ATM_LOG_TRANSACTION_START_DATE_TIME_PATTERN=r"DATE\s{1}\d{2}-\d{2}-\d{2}.*TIME\s{1}\d{2}:\d{2}:\d{2}"
    DIEBOLD_ATM_LOG_TRANSACTION_START_DATE_TIME_PATTERN=r"\d{2}\/\d{2}\/\d{4}\s{1}\d{2}:\d{2}:\d{2}\s{1}Card Inserted"
    #DIEBOLD_ATM_LOG_TRANSACTION_START_DATE_TIME_PATTERN=r"\d{2}\/\d{2}\/\d{4}\s{1}\d{2}:\d{2}:\d{2}\s{1}\d{2}\/\d{2}\/\d{4}:\d{2}:\d{2,6}"

    NCR_ATM_LOG_TRANSACTION_END_DATE_TIME_PATTERN=r"\d{2}:\d{2}:\d{2}\s{1}TRANSACTION END"
    DIEBOLD_ATM_LOG_TRANSACTION_END_DATE_TIME_PATTERN=r"(\d{2}\/\d{2}\/\d{4}\s{1}\d{2}:\d{2}:\d{2}\s{1}RESPONSE)|(\d{2}\/\d{2}\/\d{4}\s{1}\d{2}:\d{2}:\d{2}\s{1}Card Ejected)"

    CARDLESS_TRANSACTION=r"CARDLESS TRANSACTION START"
    #CARDLESS, CARD

    NCR_ATM_LOG_TRANSACTION_CARD_NUMBER_PATTERN=r"\d{6,8}X{5,7}\d{3,5}"
    DIEBOLD_ATM_LOG_TRANSACTION_CARD_NUMBER_PATTERN = r"\d{5,7}X{5,7}\d{3,5}"