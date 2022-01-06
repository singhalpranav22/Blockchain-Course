// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage{
    uint256 public favNumber = 5;
    bool favBool = true;
    string favString = "Hello World";
    int256 favInt = 10;
    address favAddress = 0x752C222B61a0b420B979103Db733522Cc2dcE15e;
    function store(uint256 _favNumber) public {
        favNumber = _favNumber;
    }
    function retrieve() public view returns(uint256){
        return favNumber;
    }
    mapping(string => uint256) public nameToFavNum;
    struct People{
        string name;
        uint256 favNumber;
    }
    People[] public people;
    function addPersonn(string memory _name,uint256 _favNumber) public {
        people.push(People(_name,_favNumber));
        nameToFavNum[_name] = _favNumber;
    }
}