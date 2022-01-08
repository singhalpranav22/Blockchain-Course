// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

interface AggregatorV3Interface {
  function decimals() external view returns (uint8);

  function description() external view returns (string memory);

  function version() external view returns (uint256);

  // getRoundData and latestRoundData should both raise "No data present"
  // if they do not have data to report, instead of returning unset values
  // which could be misinterpreted as actual reported values.
  function getRoundData(uint80 _roundId)
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
}

contract FundMe{

    address public owner;
    AggregatorV3Interface priceFeed;
    constructor(address _ethChainlink) {
        priceFeed = AggregatorV3Interface(_ethChainlink);
        owner = msg.sender;
    }
    mapping(address => uint256) public addressToAmountFunded;
    function fund() public payable {
         uint256 minUsd = 50;
    require(getUsdRate(msg.value)>=minUsd);
        addressToAmountFunded[msg.sender] += msg.value;
    }
    function getVersion() public view returns(uint256){
        return priceFeed.version();
    }

    function getPrice() public view returns(int256){
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

    function getEntranceFee() public view returns(uint256){
      // minimumusd 
      uint256 minUsd = 50*10**18;
      uint256 price = (uint256(getPrice()));
      uint256 precision = 1 * 10**18; 
      return (minUsd * precision)/ price;

    }
}
