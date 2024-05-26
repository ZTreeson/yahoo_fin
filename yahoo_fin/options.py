

import pandas as pd
import numpy as np
import requests
from pathlib import Path

try:
    from requests_html import HTMLSession
except Exception:
    pass

#setting
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',None)

def force_float(elt):
    
    try:
        return float(elt)
    except:
        return elt

def build_options_url(ticker, date = None):
    
    """Constructs the URL pointing to options chain"""
       
    url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker

    if date is not None:
        url = url + "&date=" + str(int(pd.Timestamp(date).timestamp()))
    print(url)

    return url

def get_options_chain(ticker, date = None, raw = True, headers = {'User-agent': 'Mozilla/5.0'}):
    
    """Extracts call / put option tables for input ticker and expiration date.  If
       no date is input, the default result will be the earliest expiring
       option chain from the current date.
    
       @param: ticker
       @param: date"""    
    
    site = build_options_url(ticker, date)
    print('get_options_chain url: ',site)
    tables = pd.read_html(requests.get(site, headers=headers).text)
    #print('table: ', tables)
    #print(tables[0],type(tables))
    if len(tables) == 1:
        calls = tables[0].copy()
        #puts = pd.DataFrame(columns = calls.columns)
        puts = pd.DataFrame()
    else:
        calls = tables[0].copy()
        puts = tables[1].copy()
        #print(tables,type(tables))

    #filepath = Path('/Users/treeson/Documents/out.csv')
    #filepath.parent.mkdir(parents=True, exist_ok=True)
    #print('path: ', filepath)
    #puts.to_csv(filepath)
    
    if not raw:
        calls["% Change"] = calls["% Change"].str.strip("%").map(force_float)
        calls["% Change"] = calls["% Change"].map(lambda num: num / 100 if isinstance(num, float) else 0)
        calls["Volume"] = calls["Volume"].str.replace("-", "0").map(force_float)
        calls["Open Interest"] = calls["Open Interest"].str.replace("-", "0").map(force_float)
        
        
        puts["% Change"] = puts["% Change"].str.strip("%").map(force_float)
        puts["% Change"] = puts["% Change"].map(lambda num: num / 100 if isinstance(num, float) else 0)
        puts["Volume"] =puts["Volume"].str.replace("-", "0").map(force_float)
        puts["Open Interest"] = puts["Open Interest"].str.replace("-", "0").map(force_float)
        
    
    
    return {"calls": calls, "puts":puts}    
    
    
def get_calls(ticker, date = None):

    """Extracts call option table for input ticker and expiration date
    
       @param: ticker
       @param: date"""
       
    options_chain = get_options_chain(ticker, date)
    
    return options_chain["calls"]
    
    

def get_puts(ticker, date = None):

    """Extracts put option table for input ticker and expiration date
    
       @param: ticker
       @param: date"""
    
    options_chain = get_options_chain(ticker, date)
    
    return options_chain["puts"]    

    
def get_expiration_dates(ticker):

    """Scrapes the expiration dates from each option chain for input ticker
    
       @param: ticker"""
    
    site = build_options_url(ticker)
    
    session = HTMLSession()
    resp = session.get(site)
    
    html = resp.html.raw_html.decode()
    
    splits = html.split("</option>")
    
    dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
    
    dates = [elt for elt in dates if elt != '']
    
    session.close()
    
    return dates
    

def get_closest_price_options_contract(ticker,date,current_price): #Sample: "TSLA","17/05/24"
    option=get_options_chain(ticker,date)
    calls=option.get('calls') #return pandas.core.frame.DataFrame
    #print(calls,type(calls))
    df_closest = calls.iloc[(calls['Strike']-current_price).abs().argsort()[:1]]
    #print(df_closest,type(df_closest))
    return df_closest #return pandas.core.frame.DataFrame
    

#get_closest_price_options_contract("TSLA","17/05/24",156)
#Nj_AXW4mECWd7KaCrHfQ
    
    
    
    
    

    
