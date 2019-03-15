##############################################################################
# Main file                                                                  #
# handle argument and define route urls                                      #
##############################################################################

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.restful import Api, Resource
from flask_table import Table, Col, LinkCol
from resource import ping
from resource import show_tables
from resource import describe_table
from resource import sql_list
from resource import sql
from resource import sql_update
from resource import sql_update_item
from resource import query
from resource import query_item
from resource import config_reload
from resource import config_dump
from resource import impala_connection_check
from resource import impala_connection_put

from handle import open_config
from handle import get_sql_items
from handle import get_sql_format_item
from handle import get_impala_conn
from handle import route_delete_sql_format
from handle import route_update_sql_format
from handle import route_add_sql_format
from handle import route_reload_config
from handle import route_dump_to_config
from handle import route_check_impala_connection
from handle import route_put_impala_connection

import parm
import argparse
import util
import json

######################################################
# handle arguments                                   #
######################################################

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="Which type can choose common/adjust.", default="adjust")
parser.add_argument("--admin", type=str, help="the admin password.", default="admin")
args = parser.parse_args()
parm.ADMIN_CODE = args.admin
if args.type == "adjust":
    parm.TYPE = parm.TYPE_ADJUST
elif args.type == "common":
    parm.TYPE = parm.TYPE_COMMON
else:
    print "type is not valid"
    exit(1)

app = Flask(__name__)
api = Api(app)

######################################################
# route defined by flask restful, no web UI          #
######################################################

api.add_resource(ping, '/ping')
api.add_resource(show_tables, '/show_tables')
api.add_resource(describe_table, '/describe_table')
api.add_resource(sql_list, '/sql_list')
api.add_resource(sql, '/sql_list/<string:sql_id>')
api.add_resource(query, '/query')
api.add_resource(sql_update, '/sql_update')
api.add_resource(sql_update_item, '/sql_update/<string:sql_name>')
api.add_resource(query_item, '/query/<string:sql_name>')
api.add_resource(config_reload, '/config_reload')
api.add_resource(config_dump, '/config_dump')
api.add_resource(impala_connection_check, '/impala/connection/check')
api.add_resource(impala_connection_put, '/impala/connection/put')


######################################################
# route defined by original flask, with web UI       #
######################################################

class Result(Table):
    name = Col('SQL name')
    describe = Col('SQL desribe')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(name='name'))

# login page, need admin user and admin password to enter into sql tables page
@app.route('/index', methods=['GET','POST'])
def admin_index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username != parm.ADMIN_USER or password != parm.ADMIN_PASS:
            return redirect(url_for('admin_index'))
        # session['user'] = username
        # session.permanent = True
        return redirect(url_for('sql_table'))

# sql_table page, show overall table for sql_format
@app.route('/sql/table', methods=['GET','POST'])
def sql_table():
    if request.method == 'GET':
        sql_items = get_sql_items()
        table = Result(sql_items)
        table.border = True
        return render_template('tables.html', table=table)
    else:
        add = request.form.get('add')
        addmore = request.form.get('addmore')
        dump = request.form.get('dump')
        db = request.form.get('database')

        if add is not None:
            return redirect(url_for('sql_add'))
        if addmore is not None:
            return redirect(url_for('sql_multi_add'))
        if dump is not None:
            return redirect(url_for('sql_dump'))
        if db is not None:
            return redirect(url_for('database_connection'))

# sql_update page, used for update an existing sql item
@app.route('/sql/table/<string:name>', methods=['GET', 'POST'])
def edit(name):
    # print name
    if request.method == 'GET':
        item = get_sql_format_item(name)
        f_temp = item['filter']
        f = json.dumps(f_temp, indent=4)

        return render_template('sql_update.html', name=name, syntax=item['format'], describe=item['describe'], filter=f)
    else:
        sql_syntax = request.form.get('sql_syntax')
        sql_describe = request.form.get('sql_describe')
        sql_filter = request.form.get('sql_filter')
        sql_key = request.form.get('sql_key')
        update = request.form.get('update')
        delete = request.form.get('delete')
        back = request.form.get('back')

        if back is not None:
            return redirect(url_for('sql_table'))
        if delete is not None:
            err = route_delete_sql_format(str(sql_key), name)
            if err == "":
                return redirect(url_for('sql_table'))
            else:
                return err, parm.ERR_USER
        if update is not None:
            try:
                s_filter = json.loads(sql_filter)
            except Exception, err:
                return 'filter format err: %s' % str(err), parm.ERR_USER
            else:
                op = {
                    'sql_name': name,
                    'sql_exec': sql_syntax,
                    'sql_describe': sql_describe,
                    'sql_filter': s_filter,
                }
                err = route_update_sql_format(str(sql_key), op, parm.CONFIG_CALL_TYPE_UI)
                if err == "":
                    return redirect(url_for('sql_table'))
                else:
                    return err, parm.ERR_USER

# sql_add page, used for add a new sql item into sql_format
@app.route('/sql/add', methods=['GET','POST'])
def sql_add():
    if request.method == 'GET':
        return render_template('sql_add.html')
    else:
        sql_name = request.form.get('sql_name')
        sql_syntax = request.form.get('sql_syntax')
        sql_describe = request.form.get('sql_describe')
        sql_filter = request.form.get('sql_filter')
        sql_key = request.form.get('sql_key')
        add = request.form.get('add')
        back = request.form.get('back')

        if back is not None:
            return redirect(url_for('sql_table'))
        if add is not None:
            try:
                s_filter = json.loads(sql_filter)
            except Exception, err:
                return 'filter format err: %s' % str(err), parm.ERR_USER
            else:
                op = {
                    'sql_name': sql_name,
                    'sql_exec': sql_syntax,
                    'sql_describe': sql_describe,
                    'sql_filter': s_filter,
                }
                operation = []
                operation.append(op)
                err = route_add_sql_format(str(sql_key), operation, parm.CONFIG_CALL_TYPE_UI)
                if err == "":
                    return redirect(url_for('sql_table'))
                else:
                    return err, parm.ERR_USER

# sql_multi_add page, used for add a list of sql items info sql_format
@app.route('/sql/add/multi', methods=['GET','POST'])
def sql_multi_add():
    if request.method == 'GET':
        return render_template('sql_multi_add.html')
    else:
        sql_operation = request.form.get('sql_operation')
        sql_key = request.form.get('sql_key')
        add = request.form.get('add')
        back = request.form.get('back')

        if back is not None:
            return redirect(url_for('sql_table'))
        if add is not None:
            try:
                operation = json.loads(sql_operation)
            except Exception, err:
                return 'sql operation format err: %s' % str(err), parm.ERR_USER
            else:
                err = route_add_sql_format(str(sql_key), operation, parm.CONFIG_CALL_TYPE_UI)
                if err == "":
                    return redirect(url_for('sql_table'))
                else:
                    return err, parm.ERR_USER

# database_connection page, used for check/update database connection information
@app.route('/database/connection', methods=['GET','POST'])
def database_connection():
    if request.method == 'GET':
        msg = "show operation result"
        host, port = get_impala_conn()
        return render_template('impala_connection.html', msg=msg, host=host, port=str(port))
    else:
        sql_key = request.form.get('sql_key')
        host = request.form.get('host')
        port = util.unicode_to_int(request.form.get('port'))
        connect = request.form.get('connect')
        update = request.form.get('update')
        back = request.form.get('back')

        if back is not None:
            return redirect(url_for('sql_table'))
        if connect is not None:
            err = route_check_impala_connection(sql_key, host, port, parm.CONFIG_CALL_TYPE_UI)
            if err == "":
                msg = 'check connection: ok'
            else:
                msg = 'check connection err: %s' % err
            return render_template('impala_connection.html', msg=msg, host=host, port=port)
        if update is not None:
            err = route_put_impala_connection(sql_key, host, port, parm.CONFIG_CALL_TYPE_UI)
            if err == "":
                msg = 'update connection info: ok'
            else:
                msg = 'update connection info err: %s' % err
            return render_template('impala_connection.html', msg=msg, host=host, port=port)

# sql_dump page, used for load sql_format from config.json file or dump sql_format into config.json file
@app.route('/sql/dump', methods=['GET','POST'])
def sql_dump():
    if request.method == 'GET':
        msg = "show operation result"
        return render_template('sql_dump.html', msg=msg)
    else:
        sql_key = request.form.get('sql_key')
        dump = request.form.get('dump')
        load = request.form.get('load')
        back = request.form.get('back')

        if back is not None:
            return redirect(url_for('sql_table'))
        if load is not None:
            err = route_reload_config(str(sql_key))
            if err == "":
                msg = 'load from config file: OK'
            else:
                msg = 'load form config file err: %s' % err
            return render_template('sql_dump.html', msg=msg)
        if dump is not None:
            err = route_dump_to_config(str(sql_key))
            if err == "":
                msg = 'dump to config file: OK'
            else:
                msg = 'dump to config file err: %s' % err
            return render_template('sql_dump.html', msg=msg)


######################################################
# entry                                              #
######################################################

if __name__ == '__main__':
    print 'start restful, type is %s' % util.type_to_string(parm.TYPE)
    open_config()
    app.run(host="::", threaded=True)
