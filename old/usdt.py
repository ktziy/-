import requests
import json
class usdt:
    def huilv():
        proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}
        huilv=requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USDT",proxies=proxies, verify=False).json()
        return float(huilv['data']['rates']['CNY'])
    def query(address):
        proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}
        more=requests.get("https://apilist.tronscanapi.com/api/accountv2?address={}".format(address),proxies=proxies, verify=False).json()
        rep={
            '所有转入':more['transactions_in'],
            '所有转出':more['totalTransactionCount'],
            'usdt余额':float(more['withPriceTokens'][1]['balance'])/1000000,
            'trx余额':more['withPriceTokens'][0]['amount']
        }
        #print(more)
        return rep
    def huilv(type):#sell buy
        proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}
        huilv=requests.get(
"https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=USDT&side={}&paymentMethod=alipay&userType=blockTrade".format(type)
, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}, verify=False,proxies=proxies).json()
        all=''
        i=0
        while i <len(huilv['data'][str(type)]) and i <10:
            all+='<b>{})</b> <code>{}  {}</code>\n'.format(i,huilv['data'][str(type)][i]['nickName'],huilv['data'][str(type)][i]['price'])
            i+=1
        print(all)
        return all