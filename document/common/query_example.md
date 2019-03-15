## Query Example For Common Version

Assume we use config file like __[THIS](./config_common.json)__  
We will have 4 kinds of operations:

1) __simple sql query__

__sql format__
```json
{
  "sql_name": "sql_select1",
  "sql_exec": "SELECT $* FROM test_parquet LIMIT 5",
  "sql_describe": "select any column from table"
}
```

__input example__
```json
{
  "sql_name": "sql_select1",
  "select": "x"
}

```

__api use example__
```
curl -i -X GET http://127.0.0.1:5000/query -H "Content-Type:application/json" -d '{"sql_name":"sql_select1","select":"x"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 46
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 06:30:20 GMT

[[44131], [84853], [17911], [62645], [58607]]

```

2) __sql query with 'where'__

__sql format__
```json
{
  "sql_name": "sql_select2",
  "sql_exec": "SELECT $key|csd|csrq FROM iap_bejwt_002573_hdfs WHERE $qbgxsj.eq AND $qbrksj.eq LIMIT 5",
  "sql_describe": "select column range from key|csd|csrq where qbgxsj equal to a given number and qbrksj equal to a given number"
}
```

__input example__
```json
{
  "sql_name": "sql_select2",
  "select": "key,csd",
  "where": {
    "qbrksj": "20170818123650000",
    "qbgxsj": "20170818123650133"
  }  
}

```

__api use example__
```
curl -i -X GET http://127.0.0.1:5000/query -H "Content-Type:application/json" -d '{"sql_name":"sql_select2","select":"key,csd","where":{"qbrksj":"20170818123650000","qbgxsj":"20170818123650133"}}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 07:32:17 GMT

[["442829195911109115", ""], ["350211196509040012", ""], ["441223197407157416", ""], ["513524197501170633", ""], ["441223199309162312", ""]]

```

3) __sql inter join__

__sql format__
```json
{
  "sql_name": "sql_join1",
  "sql_exec": "SELECT test_text_merge.y FROM test_parquet,test_text_merge WHERE test_parquet.x=test_text_merge.x",
  "sql_describe": "inter join test_parquet,test_text_merge WHERE test_parquet.x=test_text_merge.x"
}
```

__input example__
```json
{
  "sql_name": "sql_join1"
}

```

__api use example__
```
curl -i -X GET http://127.0.0.1:5000/query -H "Content-Type:application/json" -d '{"sql_name":"sql_join1"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 36
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 05:57:36 GMT

[["3"], ["3"], ["2"], ["2"], ["1"]]

```

4) __sql right outer join__

__sql format__
```json
{
  "sql_name": "sql_join2",
  "sql_exec": "SELECT test_text_merge.y FROM test_parquet RIGHT OUTER JOIN test_text_merge ON test_parquet.x=test_text_merge.x",
  "sql_describe": "right outer join test_parquet,test_text_merge WHERE test_parquet.x=test_text_merge.x"
}
```

__input example__
```json
{
  "sql_name": "sql_join2"
}

```

__api use example__
```
curl -i -X GET http://127.0.0.1:5000/query -H "Content-Type:application/json" -d '{"sql_name":"sql_join2"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 36
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 08 Aug 2018 05:58:06 GMT

[["3"], ["3"], ["2"], ["2"], ["1"]]

```