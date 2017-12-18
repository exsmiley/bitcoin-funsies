# from coinbase.wallet.client import Client
# from secret import API_KEY, API_SECRET
# import json

# client = Client(API_KEY, API_SECRET)
# print client.get_buy_price(currency_pair = 'BTC-USD')
# print client.get_sell_price(currency_pair = 'BTC-USD')


# user = client.get_current_user()
# user_as_json_string = json.dumps(user)
# print user_as_json_string

import gdax
public_client = gdax.PublicClient()
lst = public_client.get_product_historic_rates('BTC-USD', granularity=60)


'''
RESPONSE ITEMS
Each bucket is an array of the following information:

time bucket start time
low lowest price during the bucket interval
high highest price during the bucket interval
open opening price (first trade) in the bucket interval
close closing price (last trade) in the bucket interval
volume volume of trading activity during the bucket interval

'''
print len(lst)
print lst[:5]