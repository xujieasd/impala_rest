##############################################################################
# this file is used to restore constant value                                #
##############################################################################

OK = 200
ERR_NOT_FIND = 404
ERR_ADMIN = 405
ERR_USER = 400
ERR_IMPALA = 407

DEF_OK = 'OK'
DEF_ERR_NOT_FIND = 'user request resource not find'
DEF_ERR_ADMIN = 'admin config file format is not correct'
DEF_ERR_USER = 'user request json format is not correct'
DEF_ERR_IMPALA = 'get an error from impala'

CONFIG_CALL_TYPE_INIT = 0
CONFIG_CALL_TYPE_REST = 1
CONFIG_CALL_TYPE_UI = 2
JSON_PATH = './config/config.json'

ERR_SUPPORT_ADJUST = "adjust version not support this api, call /query/<sql_name>"
ERR_MISS_JSON_INPUT = 'missing json input (at least input {})'
ERR_MISS_KEY_HOST = 'config.json must has key "host".'
ERR_MISS_KEY_PORT = 'config.json must has key "port".'
ERR_MISS_KEY_OPERATION = 'config.json must has key "operation".'
ERR_MISS_KEY_SQL_NAME = 'config.json.operation miss key "sql_name".'
ERR_MISS_KEY_SQL_EXEC = 'config.json.operation miss key "sql_exec".'
ERR_MISS_KEY_SQL_DESC = 'config.json.operation miss key "sql_describe".'
ERR_MISS_KEY_SQL_FILT = 'config.json.operation miss key "sql_filter".'
ERR_TYPE_ERR_INT = 'type should be int'
ERR_TYPE_ERR_STRING = 'type should be string'
ERR_TYPE_ERR_LIST = 'type should be list'
ERR_TYPE_ERR_DICT = 'type should be dict'
ERR_TYPE_ERR_JSON = 'type should be json'
ERR_ADMIN_CODE = 'the password of admin is not correct'
ERR_API_TYPE_INVALID = 'invalid api type, neither adjust nor common'
ERR_SQL_FORMAT_DELETE = 'err happened when delete sql_format'
ERR_SQL_FORMAT_UPDATE = 'err happened when update sql_format'
ERR_SQL_NAME_EXIST = 'sql name exists when add new sql item'

WARNING_MISS_CONFIG_JSON = 'config.json file not exists under directory ./config'

ADMIN_CODE = "admin"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

TYPE_COMMON = 0
TYPE_ADJUST = 1

TYPE = TYPE_COMMON
