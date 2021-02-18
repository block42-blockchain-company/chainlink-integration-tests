pragma solidity >=0.4.24 <0.8.2;
import "./ChainlinkClient.sol";

contract APITestConsumer is ChainlinkClient {
  event Wadup();

  constructor(address _link, address _oracle) public {
    setChainlinkToken(_link);
    setChainlinkOracle(_oracle);
  }

  function accpectChainLinkRequest(string memory _jobId) public {
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fullfillChainLinkRequest.selector);
    sendChainlinkRequest(req, (1 * LINK));
  }
  function fullfillChainLinkRequest() public {
    // TODO implement
  }
  function test() public returns (uint256 a){
    a = 1;
    emit Wadup();
  }
  // https://ethereum.stackexchange.com/questions/9142/how-to-convert-a-string-to-bytes32
  function stringToBytes32(string memory source) private pure returns (bytes32 result) {
    bytes memory tempEmptyStringTest = bytes(source);
    if (tempEmptyStringTest.length == 0) {
      return 0x0;
    }
    assembly {
      result := mload(add(source, 32))
    }
  }
}
