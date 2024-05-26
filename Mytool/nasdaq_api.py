import sys,os,time,re
import ssl,json,requests

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#https://stackoverflow.com/questions/62392747/timeouterror-errno-60-operation-timed-out
#test_url='https://www.nasdaq.com/market-activity/stocks/tsla/option-chain/call-put-options/tsla--240517c00185000'
test_url='https://api.nasdaq.com/api/quote/tsla/option-chain?assetclass=stocks&recordID=TSLA--240517C00185000'

def get_api_json_result(url):
    resp = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    if not resp.ok:
        raise AssertionError("""Invalid response from server.  Check if ticker is
                                  valid.""")
    json_result = resp.json()
    return json_result

def get_value_from_api_resp(api_resp):
    Call_PrevClose=api_resp["data"]["optionChainCallData"]["optionChainListData"]["PrevClose"].get('value')
    Call_Impvol=api_resp["data"]["optionChainCallData"]["optionChainGreeksList"]["Impvol"].get('value')
    Put_PrevClose = api_resp["data"]["optionChainPutData"]["optionChainListData"]["PrevClose"].get('value')
    Put_Impvol = api_resp["data"]["optionChainPutData"]["optionChainGreeksList"]["Impvol"].get('value')
    return_dict={'Call_PrevClose':Call_PrevClose,'Call_Impvol':Call_Impvol,'Put_PrevClose':Put_PrevClose,'Put_Impvol':Put_Impvol}
    return  return_dict

def get_defined_options_value(ticker,contract_no):
    contract_pre=contract_no.split('2', 1)[0]
    contract_tail='2'+contract_no.split('2', 1)[1]
    ticker_len=len(contract_pre)
    temp_profix='------'
    new_contractname=contract_pre+temp_profix[ticker_len:]+contract_tail
    print('Contract Name: ',new_contractname)
    #contract_tail=re.sub('24', '24', contract_no, count=1, flags=0)
    #print(contractname)
    api_url='https://api.nasdaq.com/api/quote/'+ticker+'/option-chain?assetclass=stocks&recordID='+new_contractname
    print('get_defined_options_value url: '+api_url)
    api_result=get_api_json_result(api_url)
    values=get_value_from_api_resp(api_result)

    return values #dict


#get_defined_options_value('tesl','TSLA240517C00180000')

#api_resp=get_api_json_result(test_url)
#result=get_value_from_api_resp(api_resp)
#print(result,type(result))