## ADMIN INPUT JSON FORMAT

### ADMIN:

Load json config when init:

#### Json format:

```json

{
  "host": "host_name",
  "port": port_number,
  "operation":[
    {
      "sql_name": "sql_name1",
      "sql_exec": "sql_exec1",
      "sql_describe": "sql_describe1",
      "sql_filter":{
          "filter1": "item1",
          "filter2": "item2"
      }
    },
    {
      "sql_name": "sql_name1",
      "sql_exec": "sql_exec1",
      "sql_describe": "sql_describe1",
      "sql_filter":{
          "filter1": "item1",
          "filter2": "item2"
      }
    }
  ]
}

```

- __"host"__ represent for impala server host, used for connect impala
- __"port" stand__ for impala server port, used for connect impala
- __"operation"__ is an array which element must contain "sql\_name", "sql\_exec", "sql\_describe"
- __"sql\_name"__ is the name/id for every sql syntax, this must be unique
- __"sql\_exec"__ is the template for sql operation which expose parameter (start with $).  
so if user want to use a particular sql_name, need to fill in the corresponding parameter
- __"sql\_describe"__ is the description for given sql syntax
- __"sql\_filter"__ will translate $Filed in "sql\_exec" to a new word,  
it's used to simplify $Filed for user, because length of $Filed from impala could be very long   
each $filterX in "sql\_filter" must exists in $FieldX in "sql\_exec"

#### sql_exec and sql_filter example

SELECT XXX FROM [TABLE] WHERE <font color="#ff0000">__$Field1.OP__</font> AND <font color="#ff0000">__$Field2.OP__</font> OR <font color="#ff0000">__$Field3.OP__</font> ORDER BY [COLUMN]  

So, corresponding sql_filter could be:

```json
{
  "sql_filter":{
          "Filed1": "item1",
          "Filed2": "item2",
          "Filed3": "item3",
      }
}
```

> __e.g__  
> __SELECT * FROM person WHERE <font color="#ff0000">$qbgxsjvbn.gt</font> AND <font color="#ff0000">$qbgxsjvbnc.eg</font>__  
> __"sql_filter":{"qbgxsjvbn": "age","qbgxsjvbnc": "workYear"}__  
> so for user's view, just need to know two parameter: age & workYear
 

#### OP definition

|OP|definition|
|-|-|
|<font color="#ff0000">__eq__</font>|Matches values that are equal to a specified value|
|<font color="#ff0000">__gt__</font>|Matches values that are great than a specified value|
|<font color="#ff0000">__gte__</font>|Matches values that are great than or equal to a specified value|
|<font color="#ff0000">__lt__</font>|Matches values that are less than a specified value|
|<font color="#ff0000">__lte__</font>|Matches values that are less than or equal to a specified value|
|<font color="#ff0000">__ne__</font>|Matches values that are not equal to a specified value|
|<font color="#ff0000">__like__</font>|Matches always cover the entire string|

> __e.g__  
> __SELECT * FROM person WHERE <font color="#ff0000">$age.gt</font> AND <font color="#ff0000">$workYear.eg</font>__  
> Means select * from _table person_ filter by _age_ great than a given number and _workYear_ equal to a given number
 

