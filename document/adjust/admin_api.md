## Admin Restful API

Admin restful API is designed for admin manage service remotely  

Admin input json should contains sql\_admin:

```json
{
  "sql_admin": "admin"
}
```

The value of "sql\_admin" is inited when impala_rest.py started, (check __`commend line options`__ in __[READ ME](../../README.md)__)  
If "sql\_admin" is not correct, you will see result like below:

```
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 52
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 15 Aug 2018 03:34:37 GMT

{"message": "the password of admin is not correct"}
```

admin restful api include:
- GET /config\_reload HTTP/1.1
- GET /config\_dump HTTP/1.1
- POST /sql\_update HTTP/1.1
- PUT /sql\_update/<sql\_name> HTTP/1.1 
- DELETE /sql\_update/<sql\_name> HTTP/1.1
- GET /impala/connection/check HTTP/1.1
- POST /impala/connection/put HTTP/1.1

### reload config.json

- GET /config\_reload HTTP/1.1  

This function will reload config.json file if config.json file changes

e.g

```
curl -i -X GET http://10.19.138.147:5000/config_reload -H "Content-Type:application/json" -d '{"sql_admin":"admin"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 15 Aug 2018 03:34:41 GMT

{"message": "done"}

```

### dump sql_format into config.json file

- GET /config\_dump HTTP/1.1

This function will record sql items from sql_format info config.json file

e.g

```
curl -i -X GET http://10.19.138.147:5000/config_dump -H "Content-Type:application/json" -d '{"sql_admin":"admin"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 22 Aug 2018 07:22:28 GMT

{"message": "done"}

```

### add sql items

- POST /sql\_update HTTP/1.1 

This function will add new items into sql\_format,  
input json format:

```json
{
  "sql_admin":"admin",
  "sql_operation":[
    {
      "sql_name":"name1",
      "sql_exec":"exec",
      "sql_describe":"description",
      "sql_filter":{
        "field1": "xxx",
        "field2": "xxx"
      }
    },
    {
      "sql_name":"name2",
      "sql_exec":"exec",
      "sql_describe":"description",
      "sql_filter":{
        "field1": "xxx",
        "field2": "xxx"
      }
    }
  ]
}
```

- Note: every sql\_name should be unique

e.g

```
curl -i -X POST http://10.19.138.147:5000/sql_update -H "Content-Type:application/json" -d '{"sql_admin":"admin","sql_operation":[{"sql_name":"test","sql_exec":"test","sql_describe":"test","sql_filter":{}}]}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 22 Aug 2018 06:30:06 GMT

{"message": "done"}

```
### update existing sql item

- PUT /sql\_update/<sql\_name> HTTP/1.1 

This function will update existing item from sql\_format,  
input json format:

```json
{
  "sql_admin":"admin",
  "sql_operation":{
    "sql_name":"xxx",
    "sql_exec":"xxx",
    "sql_describe":"xxx",
    "sql_filter":{
      "field1":"xxx",
      "field2":"xxx"
    }
  }
}
```

e.g

```
curl -i -X PUT http://10.19.138.147:5000/sql_update/test -H "Content-Type:application/json" -d '{"sql_admin":"admin","sql_operation":{"sql_name":"test","sql_exec":"test","sql_describe":"aaa","sql_filter":{"x":"x","y":"yy"}}}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 22 Aug 2018 07:05:48 GMT

{"message": "done"}

```

### delete existing sql item

- DELETE /sql\_update/<sql\_name> HTTP/1.1 

This function will delete existing item from sql\_format,  
input json format:

```json
{
  "sql_admin": "admin"
}
```

e.g

```
curl -i -X DELETE http://10.19.138.147:5000/sql_update/test1 -H "Content-Type:application/json" -d '{"sql_admin":"admin"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 22 Aug 2018 07:15:47 GMT

{"message": "done"}

```

### check impala connection

- GET /impala/connection/check HTTP/1.1

this function will check whether host and port can successfully connect to impala server  
input json format:

```json
{
  "sql_admin": "admin"
  "host": "xxx"
  "port": xxx
}
```

`host` and `port` is not required, if empty, will use `host` and `port` from local

e.g

```
curl -i -X GET http://10.19.138.147:5000/impala/connection/check -H "Content-Type:application/json" -d '{"sql_admin":"admin","host":"10.38.240.28","port":31565}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Fri, 24 Aug 2018 03:27:44 GMT

{"message": "done"}
```

```
curl -i -X GET http://10.19.138.147:5000/impala/connection/check -H "Content-Type:application/json" -d '{"sql_admin":"admin"}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Fri, 24 Aug 2018 03:28:45 GMT

{"message": "done"}
```

### update impala connection

- POST /impala/connection/put HTTP/1.1

this function will update impala host and port of local (impala_conn)  
input json format: (both host and port are required)

```json
{
  "sql_admin": "admin"
  "host": "xxx"
  "port": xxx
}
```

e.g

```
curl -i -X POST http://10.19.138.147:5000/impala/connection/put -H "Content-Type:application/json" -d '{"sql_admin":"admin","host":"10.38.240.28","port":31566}'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Fri, 24 Aug 2018 03:29:17 GMT

{"message": "done"}
```