##############################################################################
# Handle dict sql_format                                                     #
# sql_format is a dict to restore every SQL items from config.json file      #
# This file offers operations to query/add/update/delete SQL item and        #
# translate user input into SQL syntax according to corresponding SQL item   #
##############################################################################

from flask.ext.restful import abort
import json
import os
import sys
import impala_ut
import parm
from util import bool_to_string
from util import ensure_single_word

# impala_conn contains the connection parameters (host, port) for impala
# e.g {'host': '10.38.240.28', 'port': 21050}
# impala_conn should init from config.json
impala_conn = {
    'host': '',
    'port': 0,
}

# sql_format is the format for every SQL syntax, defined by admin from config.json
# sql_format['sql_name'] = {'format': 'sql_exec','describe': 'sql_describe'}
# 'sql_name' is the name/id for SQL syntax,
# 'sql_exec' is the sql syntax defined by admin,
# 'sql_describe' is the description for given sql syntax
sql_format = {
    'test': {
        'format': 'SELECT xxx for xxx WHERE $aaa.eq',
        'describe': 'this is a test, you can add new sql syntax',
        'filter': {
            'aaa': 'bbb',
        },
    },
}

# op_format match the WHERE operation of sql
# e.g 'SELECT * from [table] WHERE A.eg' means 'SELECT * from [table] WHERE A=[value]'
# so user need add {'A': value} when use restful api
op_format = {
    'eq': '=',
    'gt': '>',
    'gte': '>=',
    'lt': '<',
    'lte': '<=',
    'ne': '<>',
    'like': 'like',
}

def handle_check_config_err(call_type, msg):
    if call_type == parm.CONFIG_CALL_TYPE_INIT:
        print msg
        sys.exit(1)
    elif call_type == parm.CONFIG_CALL_TYPE_REST:
        abort(parm.ERR_ADMIN, message=msg)
    elif call_type == parm.CONFIG_CALL_TYPE_UI:
        return msg
    else:
        print 'unexpected config_call_type'
    return 'unexpected config_call_type'

# check_config_format will check format of config.json file
# config file should contains key 'host', 'port' and 'operation'
# this function will init impala_conn, and return operation
def check_config_format(f_json, call_type):

    # below keys must be contained in config file
    err = ""
    if 'host' not in f_json:
        err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_HOST)
        return None, err
    if 'port' not in f_json:
        err =handle_check_config_err(call_type, parm.ERR_MISS_KEY_PORT)
        return None, err
    if 'operation' not in f_json:
        err =handle_check_config_err(call_type, parm.ERR_MISS_KEY_OPERATION)
        return None, err

    # check whether key's type is valid
    if type(f_json['host']) is not unicode:
        err = handle_check_config_err(call_type, 'host type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return None, err
    if type(f_json['port']) is not int:
        err = handle_check_config_err(call_type, 'port type err: %s' % parm.ERR_TYPE_ERR_INT)
        return None, err
    if type(f_json['operation']) is not list:
        err = handle_check_config_err(call_type, 'operation type err: %s' % parm.ERR_TYPE_ERR_LIST)
        return None, err

    impala_conn['host'] = f_json['host']
    impala_conn['port'] = f_json['port']
    operation = f_json['operation']

    return operation, err

# check_filter_format will check format for sql_filter
# sql_filter type should be dict and each value of sql_filter should be string
def check_filter_format(filter, call_type):

    err = ""
    if type(filter) is not dict:
        err = handle_check_config_err(call_type, 'sql_filter type err: %s' % parm.ERR_TYPE_ERR_DICT)
        return err

    for f in filter:
        if type(filter[f]) is not unicode:
            err = handle_check_config_err(call_type, 'sql_filter element type err: %s' % parm.ERR_TYPE_ERR_STRING)
            return err
    return err

# check_name_unique will check if sql_name is unique when add new sql_items into sql_format
# return "" if new sql_name is valid,
def check_name_unique(operation, call_type):
    # value of key 'operation' is an array,
    err = ""
    for op in operation:
        if 'sql_name' not in op:
            err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_SQL_NAME)
            return err
        if op['sql_name'] in sql_format:
            err = handle_check_config_err(call_type, 'add %s err: %s' % (op['sql_name'], parm.ERR_SQL_NAME_EXIST))
            return err
    return err

# check_config_operation will check format of operation from config.json file
# which item contains key 'sql_name', 'sql_exec', 'sql_describe'
# if it's adjust version, also should contains key 'sql_filter'
def check_config_operation(operation, call_type):

    # value of key 'operation' is an array,
    err = ""
    for op in operation:
        err = check_config_op(op, call_type)
        if err != "":
            return err
    return err

# check_config_op will check op format for every items in operation
def check_config_op(op, call_type):
    # below keys must be contained in op
    err = ""
    if 'sql_name' not in op:
        err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_SQL_NAME)
        return err
    if 'sql_exec' not in op:
        err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_SQL_EXEC)
        return err
    if 'sql_describe' not in op:
        err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_SQL_DESC)
        return err

    # check whether key's type is valid
    if type(op['sql_name']) is not unicode:
        err = handle_check_config_err(call_type, 'sql_name type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return err
    if type(op['sql_exec']) is not unicode:
        err = handle_check_config_err(call_type, 'sql_exec type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return err
    if type(op['sql_describe']) is not unicode:
        err = handle_check_config_err(call_type, 'sql_describe type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return err

    if parm.TYPE == parm.TYPE_COMMON:
        sql_format[op['sql_name']] = {
            'format': op['sql_exec'],
            'describe': op['sql_describe'],
        }
    else:
        if 'sql_filter' not in op:
            err = handle_check_config_err(call_type, parm.ERR_MISS_KEY_SQL_FILT)
            return err
        err = check_filter_format(op['sql_filter'], call_type)
        if err != "":
            return err
        sql_format[op['sql_name']] = {
            'format': op['sql_exec'],
            'describe': op['sql_describe'],
            'filter': op['sql_filter'],
        }
    return err

# open_config is a function to load config.json file
# this function will init impala_conn and sql_format
# config format for common version:
# {
#     "host": "xxx",
#     "port": xxx,
#     "operation":[
#        {
#             "sql_name": "xxx",
#             "sql_exec": "xxx",
#             "sql_describe": "xxx"
#        }
#     ]
# }
# config format for adjust version:
# {
#     "host": "xxx",
#     "port": xxx,
#     "operation":[
#        {
#             "sql_name": "xxx",
#             "sql_exec": "xxx",
#             "sql_describe": "xxx",
#             "sql_filter":{
#                 "filter1": "xxx",
#                 "filter2": "xxx"
#             }
#        }
#     ]
# }
def open_config():
    print "open config"

    # ./config.json file should exists
    path = parm.JSON_PATH
    if os.path.exists(path) is not True:
        create_new_config(path)
    else:
        init_config(path)

# create new config.json file if file is not exists
def create_new_config(path):
    print parm.WARNING_MISS_CONFIG_JSON
    try:
        with open(path, 'w') as f:
            print "create new config.json file"
            config_dump = {}
            operation_dump = []
            config_dump['host'] = impala_conn['host']
            config_dump['port'] = impala_conn['port']
            config_dump['operation'] = operation_dump
            json.dump(config_dump, f, indent=4)
    except Exception, err:
        print "config.json create with err: %s." % str(err)
        sys.exit(1)

# load config from config.json file
def init_config(path):
    print "init read config"
    with open(path, 'rb') as f:
        try:
            f_json = json.load(f)
        except Exception, err:
            print "config.json is not valid err %s." % str(err)
            sys.exit(1)
        else:
            operation, err = check_config_format(f_json, parm.CONFIG_CALL_TYPE_INIT)
            if err != "":
                print err
                sys.exit(1)
            err = check_config_operation(operation, parm.CONFIG_CALL_TYPE_INIT)
            if err != "":
                print err
                sys.exit(1)

# if sql_name not exist in sql_format, return 404 not find
def abort_if_sql_not_exist(sql_id):
    if sql_id not in sql_format:
        abort(parm.ERR_NOT_FIND, message="sql name not defined, run /sql_list to check sql name".format(sql_id))

# return list of sql_format keys
def get_sql_format_name():
    name = [n for n in sql_format]
    return name

# get sql_format value for given sql_name key
def get_sql_format_item(sql_id):
    return sql_format[sql_id]

# get lists of sql_name & sql_description from sql_format dict
def get_sql_items():
    result = []
    for n in sql_format:
        item = {'name': n, 'describe': sql_format[n]['describe']}
        result.append(item)
    return result

# get impala connection host & port
def get_impala_conn():
    return impala_conn['host'], impala_conn['port']

# used for common version user API
# handle user input {'select': 'field1,field2'}
# 'field1,field2' should in range of admin definition $filed_range
# if $filed_range is *, can select all items in sql_select
# return is a str, e.g "SELECT field1,field2 from xxx"
def sql_handle_select(format_select, sql_select):

    if sql_select is None:
        sql_select = []

    strs = format_select.split(" ")
    for i in range(len(strs)):
        if strs[i].startswith("$"):
            strs[i] = strs[i][1:]
            # if not *, should check whether sql_select is in format select range
            if strs[i] != "*":
                format_column = strs[i].split("|")
                column_map = {}
                for f_column in format_column:
                    column_map[f_column] = 1
                for s_column in sql_select:
                    # if column_map.has_key(s_column) is not True:
                    if s_column not in column_map:
                        abort(parm.ERR_USER, message="column:%s not defined." % s_column)
            # if *, could select all items in sql_select range
            select_column = ",".join(sql_select)
            strs[i] = select_column

    res = " ".join(strs)
    return res

# used for common version user API
# handle user input {'where': {'field1': value1, 'field2': value2}}
# fieldx should defined in sql_format by admin
# return is a str, e.g "field1=A and field2>B ORDER BY xxx"
def sql_handle_filter(format_filter, sql_where):

    if sql_where is None:
        decode_sql_where = {}
    else:
        decode_sql_where = json.loads(sql_where)

    strs = format_filter.split(" ")
    for i in range(len(strs)):
        if strs[i].startswith("$"):
            strs[i] = strs[i][1:]
            ops = strs[i].split(".")
            if len(ops) != 2:
                abort(parm.ERR_ADMIN, message="sql format:%s error, please contact admin." % strs[i])
            if ops[1] not in op_format:
                abort(parm.ERR_ADMIN, message="sql format:%s error, please contact admin." % strs[i])
            if ops[0] not in sql_where:
                abort(parm.ERR_USER, message="filter:%s not complete." % ops[0])
            field = ops[0]
            op = op_format[ops[1]]
            value = decode_sql_where[ops[0]]

            # type int
            if type(value) == int:
                strs[i] = '%s%s%d' % (field, op, value)
            # type bool
            elif type(value) == bool:
                strs[i] = '%s%s%s' % (field, op, bool_to_string(value))
            # type none
            elif value is None:
                strs[i] = '%s%s%s' % (field, op, 'NULL')
            # type string
            else:
                # ensure value is a single word, to avoid hack
                if ensure_single_word(value) is not True:
                    abort(parm.ERR_USER, message="value of user filter:%s not valid." % value)
                strs[i] = '%s%s\'%s\'' % (field, op, value)

    res = " ".join(strs)
    return res

# used for adjust version user API
# handle user input {'field1': value1, 'field2': value2}
# here fieldx should match values in "sql_filter" from sql_format, e.g:
#     "sql_filter":{
#         "filter1": "field1",
#         "filter2": "field2",
#     }
# function will translate user input to sql syntax according to sql_format
# return value is a string, e.g:
# SELECT xxx FROM xxx WHERE filter1=value1 and filter2=value2
def sql_handle(sql_exec, sql_filter, args):

    if args is None:
        args = {}

    strs = sql_exec.split(" ")
    for i in range(len(strs)):
        if strs[i].startswith("$"):
            strs[i] = strs[i][1:]
            ops = strs[i].split(".")
            if len(ops) != 2:
                abort(parm.ERR_ADMIN, message="sql format:%s error, please contact admin." % strs[i])
            if ops[1] not in op_format:
                abort(parm.ERR_ADMIN, message="sql op format:%s error, please contact admin." % strs[i])
            if ops[0] not in sql_filter:
                abort(parm.ERR_ADMIN, message="sql filter:%s not complete, please contact admin." % ops[0])
            item = sql_filter[ops[0]]

            if item not in args:
                abort(parm.ERR_USER, message="user filter:%s not complete." % item)

            field = ops[0]
            op = op_format[ops[1]]
            value = args[item]

            # type int
            if type(value) == int:
                strs[i] = '%s%s%d' % (field, op, value)
            # type bool
            elif type(value) == bool:
                strs[i] = '%s%s%s' % (field, op, bool_to_string(value))
            # type none
            elif value is None:
                strs[i] = '%s%s%s' % (field, op, 'NULL')
            # type string
            else:
                # ensure value is a single word, to avoid hack
                if ensure_single_word(value) is not True:
                    abort(parm.ERR_USER, message="value of user filter:%s not valid." % item)
                strs[i] = '%s%s\'%s\'' % (field, op, value)

    res = " ".join(strs)
    return res

##################################################################
#  Restful API Called by User                                    #
##################################################################

# exec impala sql 'SHOW TABLES'
# called by show_tables.get from resource
def route_show_table():
    return impala_ut.get_tables(impala_conn['host'], impala_conn['port'])

# exec impala sql 'DESCRIBE [TABLE]'
# called by describe_table.get from resource
def route_desribe_table(sql_name, table_name):
    abort_if_sql_not_exist(sql_name)
    sql_exec = str(sql_format[sql_name]["format"])
    print sql_exec
    find = sql_exec.find("$table")
    if find == -1:
        abort(parm.ERR_ADMIN, message="sql format error, please contact admin")
    return impala_ut.describe_table(table_name, impala_conn['host'], impala_conn['port'])

# exec impala query
# called by query_item.get from resource
# handle user format
# {
#     "sql_name": "sql_name",
#     "select": "filed1,filed2,filed3",
#     "where":{
#         "filed1": value1,
#         "filed2": value2,
#         "filed3": value3
#     }
# }
def route_query_table(sql_name, sql_select, sql_where):
    abort_if_sql_not_exist(sql_name)
    sql_exec = str(sql_format[sql_name]["format"])

    # split string by ' WHERE '
    # so strs[0] handle column filter
    # and strs[1] handle row filter
    strs = sql_exec.split(" WHERE ")
    if len(strs) > 2:
        abort(405, message="sql format error, please contact admin")
    # print strs[0]
    res = sql_handle_select(strs[0], sql_select)
    # print res
    if len(strs) == 2:
        # print strs[1]
        filter = sql_handle_filter(strs[1], sql_where)
        # print filter
        res = '%s WHERE %s' % (res, filter)
    return impala_ut.query_table(res, impala_conn['host'], impala_conn['port'])

# exec simple impala query
# called by query_item.get from resource
# handle user format
# {
#     "filed1": value1,
#     "filed2": value2,
#     "filed3": value3
# }
def route_query_table_simple(sql_name, args):
    abort_if_sql_not_exist(sql_name)

    sql_exec = str(sql_format[sql_name]['format'])
    sql_filter = sql_format[sql_name]["filter"]

    res = sql_handle(sql_exec, sql_filter, args)
    return impala_ut.query_table(res, impala_conn['host'], impala_conn['port'])

##################################################################
#  Restful API Called by Admin                                   #
##################################################################

# reload config.json file, called by config_reload.get
# it is called by admin
# need first check whether admin_code is correct
def route_reload_config(admin_code):
    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE

    path = parm.JSON_PATH
    if os.path.exists(path) is not True:
        return parm.ERR_MISS_CONFIG_JSON

    with open(path, 'rb') as f:
        try:
            f_json = json.load(f)
        except Exception, err:
            return "config.json is not valid err %s." % str(err)

        else:
            global sql_format
            sql_format = {}
            operation, err = check_config_format(f_json, parm.CONFIG_CALL_TYPE_REST)
            if err != "":
                return err
            err = check_config_operation(operation, parm.CONFIG_CALL_TYPE_REST)
            return err

# dump to config will record data from sql_format into json file
# it is called by admin
# need first check whether admin_code is correct
def route_dump_to_config(admin_code):
    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE

    path = parm.JSON_PATH
    if os.path.exists(path) is not True:
        return parm.ERR_MISS_CONFIG_JSON

    with open(path, 'w+') as f:
        try:
            config_dump = {}
            operation_dump = []
            config_dump['host'] = impala_conn['host']
            config_dump['port'] = impala_conn['port']

            for sql_name in sql_format:
                operation_temp = {}
                if parm.TYPE == parm.TYPE_COMMON:
                    operation_temp = {
                        'sql_name': sql_name,
                        'sql_exec': sql_format[sql_name]['format'],
                        'sql_describe': sql_format[sql_name]['describe'],
                    }
                elif parm.TYPE == parm.TYPE_ADJUST:
                    operation_temp = {
                        'sql_name': sql_name,
                        'sql_exec': sql_format[sql_name]['format'],
                        'sql_describe': sql_format[sql_name]['describe'],
                        'sql_filter': sql_format[sql_name]['filter'],
                    }
                else:
                    return parm.ERR_API_TYPE_INVALID

                operation_dump.append(operation_temp)

            config_dump['operation'] = operation_dump
            json.dump(config_dump, f, indent=4)

        except Exception, err:
            return "dump to json file fail, err: %s." % str(err)
        
        else:
            return ""

# route_add_sql_format will add item into sql_format
# it is called by admin
# need first check whether admin_code is correct
# input operation should be json
# format: (note: it's a list)
# [
#   {
#     "sql_name": "xxx",
#     "sql_exec": "xxx",
#     "sql_describe": "xxx",
#     "sql_filter": {
#       "filter1": "item1"
#       "filter2": "item2"
#     }
#   }
# ]
def route_add_sql_format(admin_code, operations, config_type):
    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE
    if type(operations) is not list:
        err = handle_check_config_err(config_type, 'operation type err: %s' % parm.ERR_TYPE_ERR_LIST)
        return err
    try:
        decode_ops = json.dumps(operations)
    except Exception, err:
        return "%s, err: %s" % (parm.ERR_TYPE_ERR_JSON, str(err))
    else:
        err = check_name_unique(operations, config_type)
        if err == "":
            err = check_config_operation(operations, config_type)
        return err


# route_update_sql_format will update an exists item from sql_format
# it is called by admin
# need first check whether admin_code is correct
# input operation should be json
# format:
# {
#     "sql_name": "xxx",
#     "sql_exec": "xxx",
#     "sql_describe": "xxx",
#     "sql_filter": {
#       "filter1": "item1"
#       "filter2": "item2"
#     }
# }
def route_update_sql_format(admin_code, op, config_type):
    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE

    print op

    try:
        decode_op = json.dumps(op)
    except Exception, err:
        return "%s, err: %s" % (parm.ERR_TYPE_ERR_JSON, str(err))
    else:
        err = check_config_op(op, config_type)
        return err

# route_delete_sql_format will delete an exists item from sql_format
# it is called by admin
# need first check whether admin_code is correct
# sql_name should in sql_format
def route_delete_sql_format(admin_code, sql_name):
    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE
    try:
        del sql_format[sql_name]
    except Exception, err:
        return "%s, err: %s" % (parm.ERR_SQL_FORMAT_DELETE, str(err))
    else:
        return ""

# route_check_impala_connection will check whether given host and port can successfully connect to impala server
# need first check whether admin_code is correct
# if host or port is empty will use host or port from impala_conn
def route_check_impala_connection(admin_code, host, port, call_type):

    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE
    if host is None:
        host = impala_conn['host']
    if port is None:
        port = impala_conn['port']

    if type(host) is not unicode:
        err = handle_check_config_err(call_type, 'host type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return err
    if type(port) is not int:
        err = handle_check_config_err(call_type, 'port type err: %s' % parm.ERR_TYPE_ERR_INT)
        return err

    return impala_ut.check_connection(host, port)

# route_put_impala_connection will update host and port of impala_conn
# need first check whether admin_code is correct
def route_put_impala_connection(admin_code, host, port, call_type):

    if admin_code != str(parm.ADMIN_CODE):
        return parm.ERR_ADMIN_CODE

    if type(host) is not unicode:
        err = handle_check_config_err(call_type, 'host type err: %s' % parm.ERR_TYPE_ERR_STRING)
        return err
    if type(port) is not int:
        err = handle_check_config_err(call_type, 'port type err: %s' % parm.ERR_TYPE_ERR_INT)
        return err

    impala_conn['host'] = host
    impala_conn['port'] = port
    return ""
