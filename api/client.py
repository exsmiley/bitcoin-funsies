from coinbase.wallet.client import Client
from secret import API_KEY, API_SECRET
import json

client = Client(API_KEY, API_SECRET)

# user = client.get_current_user()
# user_as_json_string = json.dumps(user)
# print user_as_json_string