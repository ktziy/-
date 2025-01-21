import requests
import json

class usdt:
    # 获取USDT对CNY的汇率
    @staticmethod
    def get_huilv_rate():
        huilv = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USDT", verify=False).json()
        return float(huilv['data']['rates']['CNY'])
    # 作用同上，希望来个人下面和上面合并了
    def huilv():
        huilv = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USDT", verify=False).json()
        return float(huilv['data']['rates']['CNY'])
    # 查询账户信息
    @staticmethod
    def query(address):
        more = requests.get(f"https://apilist.tronscanapi.com/api/accountv2?address={address}", verify=False).json()
        rep = {
            '所有转入': more['transactions_in'],
            '所有转出': more['totalTransactionCount'],
            'usdt余额': float(more['withPriceTokens'][1]['balance']) / 1000000,
            'trx余额': more['withPriceTokens'][0]['amount']
        }
        return rep
    
    # 查询交易信息，type 参数是 'buy' 或 'sell'
    @staticmethod
    def get_trade_info(type):
        huilv = requests.get(
            f"https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=USDT&side={type}&paymentMethod=alipay&userType=blockTrade",
            headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}, verify=False).json()
        
        all_orders = ''
        i = 0
        while i < len(huilv['data'][str(type)]) and i < 10:
            all_orders += f"<b>{i + 1})</b> <code>{huilv['data'][str(type)][i]['nickName']}  {huilv['data'][str(type)][i]['price']}</code>\n"
            i += 1
        print(all_orders)
        return all_orders
