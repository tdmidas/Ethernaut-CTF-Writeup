# Level 6: Delegation
## ★★☆☆☆
Một challenge liên quan đến low-level function =))
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Delegate {

  address public owner;

  constructor(address _owner) {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
```
## Phân tích
Thông thường để gọi hàm từ contract B từ contract A, ta sẽ import hoặc dùng ``A.foo(x, y, z)`` nhưng Solidity cung cấp cho chúng ta một số hàm low-level khác để thay thế như:
- call()
- delegateCall()
- staticcall() 

>Tuy nhiên việc dùng các hàm này sẽ không được khuyến khích lắm vì các lý do về bảo mật như nó sẽ qua việc check hàm có tồn tại không, check kiểu dữ liệu, ...

Bạn có thể đọc thêm về các low-level call function tại [đây](https://solidity-by-example.org/call/)  


## delegateCall()
Hiểu đơn giản về ``delegateCall()`` là nếu contract A gọi ``delegateCall()`` tới contract B thì code của contract B sẽ được execute nhưng sẽ dùng storage của contract A, như trong ví dụ là ``msg.sender`` và ``msg.value``
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// NOTE: Deploy this contract first
contract B {
    // NOTE: storage layout must be the same as contract A
    uint public num;
    address public sender;
    uint public value;

    function setVars(uint _num) public payable {
        num = _num;
        sender = msg.sender;
        value = msg.value;
    }
}

contract A {
    uint public num;
    address public sender;
    uint public value;

    function setVars(address _contract, uint _num) public payable {
        // A's storage is set, B is not modified.
        (bool success, bytes memory data) = _contract.delegatecall(
            abi.encodeWithSignature("setVars(uint256)", _num)
        );
    }
}

```
## Solution
**Target**: chiếm quyền owner .  
- Trong code, ta thấy ccontract Delegate có hàm pwn() để trao quyền owner, ta cần tìm cách gọi được hàm này.
- Contract Delegation có fallback function sử dụng delegatecall, nó gợi ý cho chúng ta trigger fallback với msg.data chính là hàm pwn().
- Mặc dù fallback function trong contract Delegation không có payable,nhưng ta vẫn có thể send cho nó 0 ether để trigger =)).
- Như vậy, ta chỉ cần sendTransaction đến contract với ``msg.data`` là "pwn()" là sẽ chiếm được quyền owner của contract.  

> Lưu ý: ``msg.data`` được hash theo thuật toán SHA3 nên khi truyền "pwn()" ta cũng phải hash chuỗi này.
```javascript
await contract.sendTransaction({data:web3.utils.sha3("pwn()"})
```
Check lại xem là owner của contract chưa
```javascript
await contract.owner()
```
![Chrome console của challenge Delegate](https://minhdai-aws.s3.ap-southeast-1.amazonaws.com/delegate.png )




