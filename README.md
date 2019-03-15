# IMPALA RESTFUL API

## Features
- customized restful api for impala
 
## dependence

required: 

- impyla
- thrift
- flask
- flask-restful

## install and run

> Skip this if you don't have pip
> - wget https://bootstrap.pypa.io/get-pip.py
> - python get-pip.py

- sudo pip install impyla
- sudo pip install thrift==0.9.3
- sudo pip install flask-restful
- git clone ssh://git@gitlab.cloud.enndata.cn:10885/xujieasd/impala_rest.git
- cd impala_rest
- vi config.json (modify your config file)
- python impala_rest.py

### commend line options

```
python impala_rest.py -h
usage: impala_rest.py [-h] [--type TYPE] [--admin ADMIN]

optional arguments:
  -h, --help     show this help message and exit
  --type TYPE    Which type can choose common/adjust.
  --admin ADMIN  the admin password.

```

|arguments|type|default value|
|-|-|-|
|__type__|str|"adjust"|
|__admin__|str|"admin"|

### deploy on k8s

check __[HERE](./deploy/k8s_deploy.md)__ to deploy on k8s

## usage

check __[HERE](./common_version_usage.md)__ for common version usage

### Edit config.json 

Before run _python impala_rest.py_, you __must__ edit <font color=red>__config.json__</font> file under _impala\_rest/config_ directory  
This file is used to pass parameters to connect database and customized restful api  
You can check config.json file format __[HERE](./document/adjust/admin_intput_format.md)__  
You can refer to config.json example __[HERE](./document/adjust/config_adjust.json)__

### run common version

```
python impala_rest.py --type adjust --admin admin
```

### query restful api

GET /query/<sql_name> HTTP/1.1  

Here <sql_name> must defined in config.json file  
You can check query input json format __[HERE](./document/adjust/user_input_format.md)__  
More query example you can find __[HERE](./document/adjust/query_example.md)__

__query example:__

```
curl -i -X GET http://10.19.138.147:5000/query/sql_select0 -H "Content-Type:application/json" -d '{"item1":"20170818123650133","item2":"20170818123650000"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Tue, 14 Aug 2018 06:49:20 GMT

[["442829195911109115", ""], ["350211196509040012", ""], ["441223197407157416", ""], ["513524197501170633", ""], ["441223199309162312", ""]]

```

### check sql_name list

- GET /sql_list HTTP/1.1

get the sql_name list defined in config.json

e.g

```
curl -i -X GET http://10.19.138.147:5000/sql_list
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 109
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 15 Aug 2018 08:46:50 GMT

["sql_join1", "sql_join2", "sql_select2", "sql_select3", "sql_select0", "sql_select1", "sql_describe_table"]

```

so get sql_name list

```json
  [
    "sql_select0",
    "sql_select1",
    "sql_select2",
    "sql_select3",
    "sql_describe_table", 
    "sql_join1", 
    "sql_join2"
  ]

```

- GET /sql_list/<sql_name> HTTP/1.1

get the format (sql_exec) & description (sql_describe) & filter (sql_filter) for a given sql_name

e.g

```
curl -i -X GET http://10.19.138.147:5000/sql_list/sql_select0
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 236
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 15 Aug 2018 08:48:59 GMT

{"filter": {"qbgxsj": "item1", "qbrksj": "item2"}, "describe": "this is sql_select0 description, need fill in item1(string), item2(string)", "format": "SELECT key,csd FROM iap_bejwt_002573_hdfs WHERE $qbgxsj.eq AND $qbrksj.eq LIMIT 5"}

```

so get response

```json
{
  "describe": "this is sql_select0 description, need fill in item1(string), item2(string)", 
  "format": "SELECT key,csd FROM iap_bejwt_002573_hdfs WHERE $qbgxsj.eq AND $qbrksj.eq LIMIT 5",
  "filter": {
    "qbgxsj": "item1",
    "qbrksj": "item2"
  }
}
```

### admin api

check restful api for admin __[HERE](./document/adjust/admin_api.md)__

### admin front

we have a simple admin front UI for adjust version, so admin can easily handle config file  
check usage __[HERE](./document/adjust/admin_front.pdf)__





