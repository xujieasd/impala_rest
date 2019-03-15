##############################################################################
# Resources for flask.ext.restful                                            #
# The resource urls are defined in impala_rest file                          #
##############################################################################

from flask import Flask, request, render_template, Response, redirect, session
from flask.ext.restful import reqparse, abort, Api, Resource, fields
import json
from handle import route_show_table
from handle import route_desribe_table
from handle import route_query_table
from handle import route_query_table_simple
from handle import route_reload_config
from handle import route_dump_to_config
from handle import route_add_sql_format
from handle import route_update_sql_format
from handle import route_delete_sql_format
from handle import route_check_impala_connection
from handle import route_put_impala_connection
from handle import get_sql_format_name
from handle import get_sql_items
from handle import abort_if_sql_not_exist
from handle import get_sql_format_item
from handle import get_impala_conn

import parm

def select_list_parser(select):
    select = str(select)
    res = select.split(",")
    return res

def select_where_parser(where):
    where = json.dumps(where)
    return where

def operation(op):
    # op = json.dumps(op)
    return op

parser = reqparse.RequestParser()
parser.add_argument('sql_name', type=str, location='json')
parser.add_argument('table', type=str, location='json')
parser.add_argument('select', type=select_list_parser, location='json')
parser.add_argument('where', type=select_where_parser, location='json')

# ping just return 'ping', this resource is used to check whether server is running
class ping(Resource):
    def get(self):
        return {'result': 'ping'}, parm.OK

############################################################
#  RESOURCE Used by User                                   #
############################################################

# show_tables will show all tables name in database, equal to sql `SHOW TABLES`
class show_tables(Resource):
    def get(self):
        res, err = route_show_table()
        if err == "":
            return res, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_IMPALA

# describe_table will describe a table, equal to sql ''DESCRIBE ${table}'
# restful input json should be {"sql_name":"sql_describe_table","table":${table}}'
# e.g GET /describe_table -d '{"sql_name":"sql_describe_table","table":"test_text_merge"}'
# [["x", "int", ""], ["y", "string", ""]]
class describe_table(Resource):
    def get(self):
        args = parser.parse_args()
        sql_name = args['sql_name']
        table = args['table']
        res, err = route_desribe_table(sql_name, table)
        if err == "":
            return res, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_IMPALA

# query will query from database
# restful input json should contain 'sql_name', 'select'(not required), 'where'(not required)
# so input json format: {"sql_name":${name},"select":${columns},"where":{${field1}:${value1},${field2}:${value2}}'
# can use GET /sql_list/${name} to check the sql format
# only support for common version
class query(Resource):
    def get(self):

        if parm.TYPE == parm.TYPE_ADJUST:
            return {'warning': parm.ERR_SUPPORT_ADJUST}, parm.ERR_USER

        args = parser.parse_args()
        sql_name = args['sql_name']
        sql_select = args['select']
        sql_where = args['where']
        # print sql_name
        # print sql_select
        # print sql_where

        format, res, err = route_query_table(sql_name, sql_select, sql_where)

        if err == "":
            return res, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_IMPALA

# query_item will query from database
# call GET /query/${sqL_name} to access database
# for common version
# restful input json should contain 'sql_name', 'select'(not required), 'where'(not required)
# so input json format: {"sql_name":${name},"select":${columns},"where":{${field1}:${value1},${field2}:${value2}}'
# for adjust version
# restful input json format: {${field1}:${value1},${field2}:${value2}}
# if sql_name do not need input field you can input nothing, or just input {}
# can use GET /sql_list/${name} to check the sql format
class query_item(Resource):
    def get(self, sql_name):
        abort_if_sql_not_exist(sql_name)
        if parm.TYPE == parm.TYPE_COMMON:
            args = parser.parse_args()
            name = args['sql_name']
            select = args['select']
            where = args['where']

            format, res, err = route_query_table(name, select, where)
        else:
            try:
                args = request.get_json()
            except Exception, err:
                return {'err': str(err)}, parm.ERR_USER
            else:
                format, res, err = route_query_table_simple(str(sql_name), args)

        if err == "":
            return res, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_IMPALA

# sql_list will list all valid sql_name
# e.g GET /sql_list
# {"sql_select2", "sql_select0", "sql_describe_table", "sql_select1"}
class sql_list(Resource):
    def get(self):
        name = get_sql_format_name()
        return name, parm.OK

# sql will return the format and describe for a given sql_name
# e.g GET /sql_list/sql_select1
# {"describe": "select any column from table", "format": "SELECT $* FROM test_parquet LIMIT 5"}
class sql(Resource):
    def get(self, sql_id):
        abort_if_sql_not_exist(sql_id)
        item = get_sql_format_item(sql_id)
        return item, parm.OK

############################################################
#  RESOURCE Used by Admin                                  #
############################################################

# config_reload will reload config.json
# e.g GET /config_reload
# -d {"sql_admin": "admin"}
class config_reload(Resource):
    def get(self):
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        args = par.parse_args()
        admin = args['sql_admin']
        err = route_reload_config(admin)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_ADMIN

# config_dump will record dict sql_format into json file
# e.g GET /config_reload
# -d {"sql_admin": "admin"}
class config_dump(Resource):
    def get(self):
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        args = par.parse_args()
        admin = args['sql_admin']
        err = route_dump_to_config(admin)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_ADMIN

# sql_update will call post function to add new items into sql_format
# e.g POST /sql_update
# -d {"sql_admin": "admin", "sql_operation": [...]}
class sql_update(Resource):

    # add new sql_format item
    def post(self):
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        par.add_argument('sql_operation', type=operation, location='json', action='append', required=True)

        args = par.parse_args()
        admin = args['sql_admin']
        ops = args['sql_operation']

        err = route_add_sql_format(admin, ops, parm.CONFIG_CALL_TYPE_REST)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_USER

# sql_update_item will call put function to update exists item from sql_format
# and call delete function to delete exists item from sql_format
# e.g PUT /sql_update/<sql_name> -d {"sql_admin": "admin", "sql_operation": [...]}
# e.g DELETE /sql_update/<sql_name> -d {"sql_admin": "admin"}
class sql_update_item(Resource):

    # update a exists sql_format item
    def put(self, sql_name):
        abort_if_sql_not_exist(sql_name)
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        par.add_argument('sql_operation', type=operation, location='json', required=True)

        args = par.parse_args()
        admin = args['sql_admin']
        op = args['sql_operation']

        err = route_update_sql_format(admin, op, parm.CONFIG_CALL_TYPE_REST)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_USER

    # delete a exists sql_format item
    def delete(self, sql_name):
        abort_if_sql_not_exist(sql_name)
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)

        args = par.parse_args()
        admin = args['sql_admin']

        err = route_delete_sql_format(admin, sql_name)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_USER

# impala_connection_check will call function to check
# whether given host and port can successfully connect to impala server
# e.g GET /impala/connection/check -d {"sql_admin": "admin", "host": "xxx", "port": xxx}
# if host or port is None, e.g GET /impala/connection/check -d {"sql_admin": "admin"}
# will use host and port from local (impala_conn)
class impala_connection_check(Resource):

    def get(self):
        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        par.add_argument('host', type=unicode, location='json')
        par.add_argument('port', type=int, location='json')

        args = par.parse_args()
        admin = args['sql_admin']
        host = args['host']
        port = args['port']

        err = route_check_impala_connection(admin, host, port, parm.CONFIG_CALL_TYPE_REST)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_USER

# impala_connection_put will update host and port of local (impala_conn)
# e.g POST /impala/connection/put -d {"sql_admin": "admin", "host": "xxx", "port": xxx}
# both "host" and "port" is required
class impala_connection_put(Resource):

    def post(self):

        par = reqparse.RequestParser()
        par.add_argument('sql_admin', type=str, location='json', required=True)
        par.add_argument('host', type=unicode, location='json', required=True)
        par.add_argument('port', type=int, location='json', required=True)

        args = par.parse_args()
        admin = args['sql_admin']
        host = args['host']
        port = args['port']

        err = route_put_impala_connection(admin, host, port, parm.CONFIG_CALL_TYPE_REST)
        if err == "":
            return {'message': 'done'}, parm.OK
        else:
            return {'err': str(err)}, parm.ERR_USER
