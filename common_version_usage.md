## COMMON VERSION USAGE

### Edit config.json 

Before run _python impala_rest.py_, you __must__ edit <font color=red>__config.json__</font> file under _impala\_rest/config_ directory  
This file is used to pass parameters to connect database and customized restful api  
You can check config.json file format [here](./document/common/admin_intput_format.md)  
You can refer to config.json example [here](./document/common/config_common.json)

### run common version

```
python impala_rest.py --type common --admin admin
```

### query restful api

GET /query HTTP/1.1  

You can check query input json format [here](./document/common/user_input_format.md)  
More query example you can find [here](./document/common/query_example.md)

__query example:__

```
curl -i -X GET http://127.0.0.1:5000/query -H "Content-Type:application/json" -d '{"sql_name":"sql_select2","select":"key,csd","where":{"qbrksj":"20170818123650000","qbgxsj":"20170818123650133"}}'

```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 07:32:17 GMT

[["442829195911109115", ""], ["350211196509040012", ""], ["441223197407157416", ""], ["513524197501170633", ""], ["441223199309162312", ""]]

```

### other useful api

- GET /sql_list HTTP/1.1

get the sql_name list defined in config.json

e.g

```
curl -i -X GET http://127.0.0.1:5000/sql_list
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 79
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 03:43:59 GMT

["sql_select2", "sql_describe_table", "sql_select1", "sql_join1", "sql_join2"]

```

so get sql_name list

```json
  [
    "sql_select2", 
    "sql_describe_table", 
    "sql_select1", 
    "sql_join1", 
    "sql_join2"
  ]

```


- GET /sql_list/<sql_name> HTTP/1.1

get the format (sql_exec) and description (sql_describe) for a given sql_name

e.g

```
curl -i -X GET http://127.0.0.1:5000/sql_list/sql_select1
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 94
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Thu, 09 Aug 2018 06:34:38 GMT

{"describe": "select any column from table", "format": "SELECT $* FROM test_parquet LIMIT 5"}

```

so get response

```json
{
  "describe": "select any column from table", 
  "format": "SELECT $* FROM test_parquet LIMIT 5"
}
```
