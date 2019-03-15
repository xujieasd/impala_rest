## Query Example For Common Version

Assume we use config file like __[THIS](./config_adjust.json)__  

users can use restful api like below:

### simple query without filter

__config example__
```json
{
      "sql_name": "sql_select1",
      "sql_exec": "SELECT x FROM test_parquet2 LIMIT 5",
      "sql_describe": "select x",
      "sql_filter": {}
}
```

__input example__

NONE

__api use example__
```
curl -i -X GET http://10.19.138.147:5000/query/sql_select1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Tue, 14 Aug 2018 06:49:34 GMT

[[175575], [80212], [180425], [37339], [32862]]

```

### query with filter

__config example__
```json
{
      "sql_name": "sql_select3",
      "sql_exec": "SELECT y FROM test_text_merge WHERE $x.gt",
      "sql_describe": "need to fill in x",
      "sql_filter": {
        "x": "x"
      }
}
```

__input example__

```json
{
  "x": 1
}

```

__api use example__
```
curl -i -X GET http://10.19.138.147:5000/query/sql_select3 -H "Content-Type:application/json" -d '{"x":1}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 29
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Tue, 14 Aug 2018 07:50:07 GMT

[["3"], ["2"], ["3"], ["2"]]

```

### query with more filters

__config example__
```json
{
      "sql_name": "sql_select2",
      "sql_exec": "SELECT key,csd FROM iap_bejwt_002573_hdfs WHERE $qbgxsj.eq AND $qbrksj.eq LIMIT 5",
      "sql_describe": "select column range from key,csd where item1 equal to a given number and item2 equal to a given number",
      "sql_filter": {
        "qbgxsj": "item1",
        "qbrksj": "item2"
      }
}
```

__input example__

```json
{
  "item1": "20170818123650133",
  "item2": "20170818123650000" 
}

```

__api use example__
```
curl -i -X GET http://10.19.138.147:5000/query/sql_select2 -H "Content-Type:application/json" -d '{"item1":"20170818123650133","item2":"20170818123650000"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 141
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Tue, 14 Aug 2018 06:49:06 GMT

[["442829195911109115", ""], ["350211196509040012", ""], ["441223197407157416", ""], ["513524197501170633", ""], ["441223199309162312", ""]]

```

### join operation

__config example__
```json
{
      "sql_name": "sql_join2",
      "sql_exec": "SELECT test_text_merge.y FROM test_parquet2 RIGHT OUTER JOIN test_text_merge ON test_parquet2.x=test_text_merge.x",
      "sql_describe": "right outer join test_parquet2,test_text_merge WHERE test_parquet.x=test_text_merge.x",
      "sql_filter": {}
}
```

__input example__

NONE

__api use example__
```
curl -i -X GET http://10.19.138.147:5000/query/sql_join2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 253
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 15 Aug 2018 03:07:18 GMT

[["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["2"], ["1"], ["1"], ["1"], ["1"], ["1"], ["1"], ["1"], ["1"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"], ["3"]]

```