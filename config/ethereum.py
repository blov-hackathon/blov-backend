from web3 import Web3
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy
from web3.middleware import geth_poa_middleware
from django.conf import settings


fast_gas_price_strategy = construct_time_based_gas_price_strategy(
    10, sample_size=5, probability=98, weighted=False)
w3 = Web3(Web3.HTTPProvider(settings.ETH_RPC_URL))
w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def create_wallet():
    return w3.eth.account.create()
