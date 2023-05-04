import numpy as np
import pandas as pd


def sql_type_mapping(sql_type):
    # For create mysql_pandas the references that have been taken have been the following:
    # https://www.promotic.eu/en/pmdoc/Subsystems/Db/MsSQL/DataTypes.htm
    # https://vincentteyssier.medium.com/optimizing-the-size-of-a-pandas-dataframe-for-low-memory-environment-5f07db3d72e
    if sql_type == 'mssql':
        type_conversor = {"bigint": 'int64', "binary": 'object', "bit": 'bool', "date": 'datetime64[ns]',
                          "datetime": 'datetime64[ns]', "datetime2": 'datetime64[ns]', "datetimeoffset": 'datetime64[ns]', "decimal": 'float64',
                          "float": 'float32', "geography": 'object', "geometry": 'object', "hierarchyid": 'object', "image": 'object',
                          "int": 'int32', "money": 'float64', "nchar": 'object', "ntext": 'object', "numeric": 'float64',
                          "nvarchar": 'object', "real": 'float32', "smalldatetime": 'datetime64[ns]', "smallint": 'int8',
                          "smallmoney": 'float32', "sql_variant": 'object', "sysname": 'object', "text": 'object', "time": 'datetime64[ns]',
                          "timestamp": 'datetime64[ns]', "tinyint": 'object', "uniqueidentifier": 'object', "varbinary": 'object',
                          "varchar": 'object', "xml": 'object', "char": 'object'}
    # Documentation for create mysql_pandas dictionary has been taken from the following links:
    # https://www.w3schools.com/mysql/mysql_datatypes.asp
    elif sql_type == 'mysql':
        type_conversor = {"char": 'object', "varchar": 'object', "binary": 'object', "varbinary": 'object', "tinyblob": 'object',
                          "tinytext": 'object', "text": 'object', "blob": 'object', "mediumtext": 'object', "mediumblob": 'object',
                          "longtext": 'object', "enum": 'object', "set": 'object', "bit": 'int8', "tinyint": 'int8',
                          "bool": 'bool', "boolean": 'bool', "smallint": 'int8', "mediumint": "int16", "int": 'int16',
                          "integer": 'int32', "bigint": 'int64', "float": 'float64', "double": 'float64', "decimal": 'float64',
                          "dec": 'float64', "date": 'datime64', "datetime": 'datetime64[ns]', "timestamp": 'datetime64[ns]',
                          "time": 'datetime64[ns]', "year": 'int64', "var_string": 'object', "long": 'int32', "longlong": 'int64',
                          "int24": 'int32', "tiny": 'int8'}
    # Documentation for create postgresql_pandas dictionary has been taken from the following links:
    # https://www.psycopg.org/docs/usage.html
    # https://www.geeksforgeeks.org/postgresql-data-types/
    elif sql_type == 'postgresql':
        type_conversor = {"bool": 'bool', "real": 'float32', "double": 'float64', "smallint": 'int8', "integer": 'int32',
                          "bigint": 'int64', "numeric": 'float64', "varchar": 'object', "text": 'object', "date": 'datetime64[ns]',
                          "timetz": 'datetime64[ns]', "timestamp": 'datetime64[ns]', "timestamptz": 'datetime64[ns]', "interval": 'datetime64[ns]',
                          "character varying": 'object', "timestamp without time zone": 'datetime64[ns]', "double precision": 'float64', "datetime": 'datetime64[ns]',
                          "str": 'object', "float": 'float64', "int": 'int32'}
    return type_conversor
