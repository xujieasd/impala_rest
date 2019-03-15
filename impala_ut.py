##############################################################################
# python impala operation interface                                          #
# use official python package impyla                                         #
# need to "host", "port", "sql syntax" to execute impala SQL operation       #
##############################################################################

from impala.dbapi import connect

def check_host_not_empty(host, port):
    if host == '':
        return False
    if port == 0:
        return False
    return True

def check_connection(host, port):

    if check_host_not_empty(host, port) is not True:
        return "host or port is empty"

    try:
        connect(host=host, port=port)
    except Exception, err:
        return err
    else:
        return ""

def get_tables(host, port):

    if check_host_not_empty(host, port) is not True:
        return "", "host or port is empty"

    try:
        conn = connect(host=host, port=port)
        cur = conn.cursor()
        cur.execute('SHOW TABLES')
        res = cur.fetchall()
    except Exception, err:
        return "", err
    else:
        return res, ""

def describe_table(argv, host, port):

    if check_host_not_empty(host, port) is not True:
        return "", "host or port is empty"

    try:
        conn = connect(host=host, port=port)
        cur = conn.cursor()
        cur.execute('DESCRIBE %s' %argv)
        res = cur.fetchall()
    except Exception, err:
        return "", err
    else:
        return res, ""

def query_table(argv, host, port):

    print argv

    if check_host_not_empty(host, port) is not True:
        return "", "host or port is empty"

    try:
        conn = connect(host=host, port=port)
        cur = conn.cursor()
        cur.execute("%s" %argv)
        description = cur.description
        fetch = cur.fetchall()
    except Exception, err:
        return "", "", err
    else:
        return description, fetch, ""

def exec_table(argv, host, port):

    if check_host_not_empty(host, port) is not True:
        return "", "host or port is empty"

    try:
        conn = connect(host=host, port=port)
        cur = conn.cursor()
        cur.execute("%s" %argv)
        fetch = cur.fetchall()
    except Exception, err:
        return "", err
    else:
        return fetch, ""
