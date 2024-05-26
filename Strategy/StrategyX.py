import requests
import pandas as pd
import ftplib
import io
import re
import json
import datetime
# Needed for decrypting
import base64
import hashlib
# Need to install pycryptodome package
#from Crypto.Cipher import AES
#from Crypto.Util.Padding import unpad
# For pretty print
#from pprint import pp
import yahoo_fin.stock_info as stock_info
import yahoo_fin.options as options
import Mytool.nasdaq_api as nasdaq_api

'''
@Input (User requirement)
    1, Ticker - pull online list 
    2, Maturity date - next 2 months 3rd friday
    
    do with stock info
        col I: ln()
        col J: sd()
        col w: minu
        ranking: top 5 sd over 1 year
        
        top 5 sum up: reference info
        

@Output
    ...
'''

def get_options_greek(ticker,mat_date):
    print(' ')
    print('############################## 1, Stock Info #####################################')
    st_info=stock_info.get_data(ticker=ticker,start_date='2024-04-29')
    print(st_info,type(st_info))
    last_row=st_info.tail(1)
    adjclose=last_row['adjclose'].iloc[-1]
    #print(adjclose,type(adjclose))

    print(' ')
    print('############################## 2, Closest-price options contract #####################################')
    opt=options.get_closest_price_options_contract(ticker=ticker,date=mat_date,current_price=adjclose)
    print(opt)
    ContractName=opt['Contract Name'].iloc[-1]
    #print(ContractName,type(ContractName))

    print(' ')
    print('############################## 3, preclose & IV #####################################')
    greekvalues=nasdaq_api.get_defined_options_value(ticker,ContractName)
    print(greekvalues)


def strategyx():
    '''
    TBC
    :return:
    '''


get_options_greek('fdx','2024-05-17')