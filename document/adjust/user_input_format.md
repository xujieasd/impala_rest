## USER INPUT JSON FORMAT

### USER:

#### restful query interface

GET /query HTTP/1.1

#### Json input format

```json
{
  "filed1": value1,
  "filed2": value2,
  "filed3": value3
}
```

__note:__
- User input should match format from config.json, your can check config.json format __[HERE](./admin_intput_format.md)__
- __filedX__ should defined in "sql\_filter" which match with <font color="#ff0000">__$FieldX.OP__</font> in "sql\_exec"

e.g:

for operation:

```json
"operation":[
    {
      "sql_name": "sql_name1",
      "sql_exec": "SELECT * FROM person WHERE $qbgxsjvbn.gt AND $qbgxsjvbnc.eg",
      "sql_describe": "sql_describe1",
      "sql_filter":{
          "qbgxsjvbn": "item1",
          "qbgxsjvbnc": "item2"
      }
    }
  ]
```

user input should be:

```json
{
  "item1": value1,
  "item2": value2
}

```



