// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "./SimpleStorage.sol";

contract StorageFactory{
    SimpleStorage[] public simpleStorageArr;

    function addSimpleStorageContract() public {
    simpleStorageArr.push(new SimpleStorage());
    }

    function storeFunOnIndex(uint256 _index,uint256 _favNumber) public{
        simpleStorageArr[_index].store(_favNumber);
    }
    function retrieveFunOnIndex(uint256 _index) public view returns(uint256){
        return simpleStorageArr[_index].retrieve();
    }

}
