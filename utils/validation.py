import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation
import numpy as np
from decimal import *

def check_decimal(dec):
    try:
        Decimal(dec)
    except InvalidOperation:
        return False
    return True
def check_int(num):
    try:
        int(num)
    except ValueError:
        return False
    return True

def check_date(da):
    try:
        pd.to_datetime(da)
    except Exception:
        return False
    return True

def isEmptyString(str):
    try:
        if(str == "" or str == null):
            return False
        else:
            return True
    except Exception:
        return False

#Create a schema for the expected csv input and use it to valdiate the input tables
def validate_file(dataframe):
    
    #define validators
    decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'is not decimal')]
    int_validation = [CustomElementValidation(lambda i: check_int(i), 'is not integer')]
    date_validation = [CustomElementValidation(lambda d: check_date(d), 'is not a date')]
    null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
    string_validation = [CustomElementValidation(lambda d: not isEmptyString(d), 'this field cannot be empty')]

    #create table schema
    schema = pandas_schema.Schema([
            Column(0, int_validation + null_validation),
            Column(1, date_validation),
            Column(2, string_validation),
            Column(3, string_validation),
            Column(4, int_validation + null_validation),
            Column(5, string_validation)
    ])

    #validate
    errors = schema.validate(dataframe)

    return errors