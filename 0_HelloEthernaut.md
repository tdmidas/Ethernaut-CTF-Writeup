# Requirement



Trước khi vào làm các challenge ta cần một số thứ như sau:
- Metamask
- Sepolia network để lấy vài test ether: https://sepoliafaucet.com/
- Remix IDE (IDE để viết contract, compile, deploy,...): https://remix.ethereum.org/

# Level 0: Hello Ethernaut
Chúng ta sẽ bắt đầu với một warmup challenge trước
## Solution

Gợi ý của challenge là bắt đầu với ```contract.info()``` trong console của Chrome, làm theo hướng dẫn ta sẽ được như sau:

```javascript

await contract.info()
"You will find what you need in info1()."

```
```javascript
await contract.info1()
"Try info2(), but with "hello" as a parameter."
```
```javascript

await contract.info2("hello")
"The property infoNum holds the number of the next info method to call."
```
Nhìn trong array, ta biết được phương thức sẽ gọi tiếp theo là ``info42()``
```javascript

await contract.infoNum()
t {s: 1, e: 1, c: Array(1)}
c: [42]
e: 1
s: 1
__proto__: Object
```

```javascript
await contract.info42()
"theMethodName is the name of the next method."
```
Tiếp tục gọi tới ```contract.theMethodName```
```javascript

await contract.theMethodName()
"The method name is method7123949."
```


```javascript
await contract.method7123949()
"If you know the password, submit it to authenticate()."
```

Sau khi gọi xong phương thức, ta để ý contract có phương thức password, gọi phương thức password và submit nó vào ```contract.authenticate``` thôi.

```
await contract.password()
"ethernaut0"
```
```
await contract.authenticate("ethernaut0")
```
Submit instance ==> **Done**

## Source code của challenge
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Instance {

  string public password;
  uint8 public infoNum = 42;
  string public theMethodName = 'The method name is method7123949.';
  bool private cleared = false;

  // constructor
  constructor(string memory _password) {
    password = _password;
  }

  function info() public pure returns (string memory) {
    return 'You will find what you need in info1().';
  }

  function info1() public pure returns (string memory) {
    return 'Try info2(), but with "hello" as a parameter.';
  }

  function info2(string memory param) public pure returns (string memory) {
    if(keccak256(abi.encodePacked(param)) == keccak256(abi.encodePacked('hello'))) {
      return 'The property infoNum holds the number of the next info method to call.';
    }
    return 'Wrong parameter.';
  }

  function info42() public pure returns (string memory) {
    return 'theMethodName is the name of the next method.';
  }

  function method7123949() public pure returns (string memory) {
    return 'If you know the password, submit it to authenticate().';
  }

  function authenticate(string memory passkey) public {
    if(keccak256(abi.encodePacked(passkey)) == keccak256(abi.encodePacked(password))) {
      cleared = true;
    }
  }

  function getCleared() public view returns (bool) {
    return cleared;
  }
}
```

