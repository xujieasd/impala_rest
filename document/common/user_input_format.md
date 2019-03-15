## USER INPUT JSON FORMAT

### USER:

#### restful query interface

GET /query HTTP/1.1

#### Json input format

```json
{
  "sql_name": "sql_name",
  "select": "filed1,filed2,filed3",
  "where":{
    "filed1": value1,
    "filed2": value2,
    "filed3": value3
  }
}
```

__note:__
- User input should match format from config.json, your can check config.json format __[HERE](./admin_intput_format.md)__
- __sql_name__ should match one of the "sql\_name" in config.json
- __filedX__ in <font color="#0000ff">__select__</font> should in range of <font color="#ff0000">__$Field\_range__</font> (defined by config.json)
- __filedX__ in <font color="#0000ff">__where__</font> should defined in "sql\_exec" which match with <font color="#ff0000">__$FieldX.OP__</font>



