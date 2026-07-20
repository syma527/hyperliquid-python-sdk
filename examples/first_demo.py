from hyperliquid.info import Info
from hyperliquid.utils import constants

from pprint import pprint
info = Info(constants.TESTNET_API_URL, skip_ws=True)
user_state = info.user_state("0x7237452d6A4d8D8B7B32A83868E82A1eBf1d58ce")

ip = info.perp_dexs()

# pprint(user_state)
pprint(ip)