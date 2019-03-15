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
      "sql_describe": "sql_describe1"
    },
    {
      "sql_name": "sql_name1",
      "sql_exec": "sql_exec1",
      "sql_describe": "sql_describe1"
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

#### sql_exec example

SELECT <font color="#ff0000">__$Field\_range__</font> FROM [TABLE] WHERE <font color="#ff0000">__$Field1.OP__</font> AND <font color="#ff0000">__$Field2.OP__</font> OR <font color="#ff0000">__$Field3.OP__</font> ORDER BY [COLUMN]

#### Field_range definition

|Field_range|definition|
|-|-|
|*|can select any columns|
|field1&#124;field2&#124;field3|only can select from field1,field2,field3|

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
> __SELECT <font color="#ff0000">$\*</font> FROM person WHERE <font color="#ff0000">$age.gt</font> AND <font color="#ff0000">$workYear.eg</font>__  
> Means user can select any column from _table person_ filter by _age_ great than a given number and _workYear_ equal to a given number
 

