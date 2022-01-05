// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe{

    address public owner;
    constructor(){
        owner = msg.sender;
    }
    mapping(address => uint256) public addressToAmountFunded;
    function fund() public payable {
         uint256 minUsd = 50;
    require(getUsdRate(msg.value)>=minUsd);
        addressToAmountFunded[msg.sender] += msg.value;
    }
    function getVersion() public view returns(uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns(int256){
         AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound 
        ) = priceFeed.latestRoundData();
        return answer*100000000;
    }
    function getUsdRate(uint256 weii) public view returns(uint256){
        uint256 priceUsd = uint256(getPrice());
        return (weii*priceUsd)/(10**18);
    } 

    function withdraw() payable public  {
        require(msg.sender==owner);
        payable(msg.sender).transfer(address(this).balance);
    }
}
