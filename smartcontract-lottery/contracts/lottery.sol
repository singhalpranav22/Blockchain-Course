// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
contract Lottery is VRFConsumerBase{
    enum LotteryStates{
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    address private owner;
    uint256 public fee;
    bytes32 keyHash;
    uint256 randomness;
    address  payable public recentWinner;
    LotteryStates lotteryState;
    AggregatorV3Interface internal priceFeed;
    event RequestedRandomness(bytes32 requestId);
    // to keep track of players  
    address payable[] public  players; 
    uint256 public minimumUsdEntrance;
    constructor (address _priceFeedAddress,address _vrfCoordinator,address _linkAddress,uint256 _fee,bytes32 _keyHash) public
    VRFConsumerBase(_vrfCoordinator,_linkAddress)
    {
       minimumUsdEntrance = 50*(10**18);
       priceFeed = AggregatorV3Interface(_priceFeedAddress); 
       lotteryState = LotteryStates.CLOSED;
       owner = msg.sender;
       fee = _fee;
       keyHash = _keyHash;
    }
    function enter() public payable{
        // to add the sender to the list of players
        // in the first slot of the array
        require(lotteryState == LotteryStates.OPEN);
        require(msg.value>=getEntranceFee(),"You need to pay at least $50 worth of ethereum to enter!");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns(uint256){
    (,int256 answer,,,) = priceFeed.latestRoundData();
     uint256 ethToDollar = uint256(answer) * (10**10); // to make it 18 decimals
     // answer dollar per eth 
     // like 2000 dollar per eth  
     // 50 dollar = 50/2000
     uint256 costToEnter = (minimumUsdEntrance * (10**18)) / ethToDollar;
    return costToEnter;
    }

    function startLottery() public {
        require(msg.sender == owner,"Only the owner can start the lottery!");
        require(lotteryState == LotteryStates.CLOSED,"Lottery is already open!");
        lotteryState = LotteryStates.OPEN;
    }

    function endLottery() public {
        require(msg.sender == owner,"You must be the owner to end the lottery!");
        // making a random number in the blockchain is very difficult or infact impossible
        // dirty way is to hash a number of values as follows 
        // uint256(
        //     keccak256(abi.encode(
        //         nonce, // transac number
        //         block.number, // predicatable
        //         msg.sender, // predicatable
        //         block.timestamp, // predicatable
        //         block.difficulty, // can be manipulated by the miners!

        //     )
        // )) % players.length;
        // change the state 
        lotteryState = LotteryStates.CALCULATING_WINNER;
        // get the winner
        bytes32 requestId = requestRandomness(keyHash,fee);
        emit RequestedRandomness(requestId);
        // wait for the randomness to be ready in fulfillRandomness
    }
    event WinnerEvent(address winner);
    function fulfillRandomness(bytes32 requestId, uint256 _randomness) internal override {
      require(lotteryState == LotteryStates.CALCULATING_WINNER,"Lottery is not in calculating state!");
      require(_randomness > 0,"Randomness must be greater than 0!");
      uint256 winnerIndex = _randomness % players.length;
      address payable winner = players[winnerIndex];
      recentWinner = winner;
      recentWinner.transfer(address(this).balance);
       emit WinnerEvent(recentWinner);
      players = new address payable[](0);
      lotteryState = LotteryStates.CLOSED;
      randomness = _randomness;
    }
}
