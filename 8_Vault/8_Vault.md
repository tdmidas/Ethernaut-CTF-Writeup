# Level 8: Vault
## ★★☆☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
```
## Phân tích

- Chúng ta đều biết mọi thứ trên blockchain đều là public, nghĩa là dù đó là những biến ``private`` hay ``internal`` nhưng ta vẫn có thể lấy data được.  

- Web3js cung cấp cho ta một phương thức lấy data là ``getstorageAt()`` -> từ đó ta có thể xem data của các biến trong contract
 

Bạn có thể xem ví dụ về ``getstorageAt()`` tại [đây](https://solidity-by-example.org/hacks/accessing-private-data/)  


## Storage structure
- Mỗi smart contract chạy trên Ethereum đều được cấp một dung lượng nhớ nhất định gọi là storage. Storage này có tổng cộng tất cả 
2^256 slot nhớ, tương đương với khoảng 10^77 slot nhớ. ( một con số rất lớn nhỉ).
- Các slot trong storage được lưu tuần tự từ slot 0 trở đi và mỗi slot lưu được tối đa 32 byte (256 bit).
- Bạn có thể xem hình dưới đây để hiểu rõ hơn:
![](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*wY8Si-mt_QZWqg0jnEDw8A.jpeg)


## Solution
**Target**: tìm password và unlock vault.  
- Ta thấy trong contract, biến ``locked`` được nhớ ở slot 0, còn ``password`` thì slot 1, ta sẽ tiến hành lấy data như sau

```javascript
web3.eth.getStorageAt("contract.address", 1, console.log)

```
- Vì password được lưu ở type là byte32, ta dùng ``web3.utils.hexToAscii ``để decode sang ASCII, ta được password là ``“A very strong secret password :)”``.  

- Gọi tới phương thức ``contract.unlock()`` để unlock vault thôi.

**Submit** -> Done
## Reference

https://kiendt.me/2018/05/01/smart-contract-storage/  

https://solidity-by-example.org/hacks/accessing-private-data/



