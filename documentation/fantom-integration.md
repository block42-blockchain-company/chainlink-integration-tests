# Fulfill Chainlink requests at fantom

With chainlink you can 
 - get Crypto prices in your smart contracts
 - generate verifable random numbers
 - call external APIs from smart contracts

Follow this guide how you can do this. 

Prerequests:
 - a running chainlink node ([setup guide](https://docs.chain.link/docs/running-a-chainlink-node))


## 1. Deploy an Oracle
You can use the [linked solidity smart contract](../contracts/Oracle/Oracle.sol) as your oracle and deploy it to the fantom network.

Later you can send your requests to this deployed smart contract. 

## 2. Add your node to the Oracle contract
To allow your node sending back the response to the oracle contract you have to grant the acces in the oracle contract. 

Therefore call the oracle contract function `setFulfillmentPermission(chainlink_address, true)` 

You can find the chainlink_address in the chainlink node GUI at the config page. 

## 3. Add jobs to the chainlink node
In the chainlink node GUI you can setup different jobs easely. Every job has at least one initiator and one task.

 - From the admin dashboard, click on New Job.
 - Paste the job from below example into the text field.
 - Click Create Job and you'll be notified of the new JobID creation. Take note of this JobID as you'll need it later.

Example job (replace {oracle_address} below with the address of your deployed oracle contract):
```json
{
   "initiators": [
   {
      "type": "runlog",
      "params": {
         "address": "{oracle_address}"
       }
   }], "tasks": [
   {
       "type": "httpget"
   },
   {
       "type": "jsonparse"
   },
   {
       "type": "ethbytes32"
   },
   {
       "type": "ethtx"
   }]
}

```

## 4. Oracle consumer
In your smart contract, now you can send a request to the deployed oracle contract (see example below).
The example contract implements ChainlinkClient and Ownable. You can find the whole example [here](../contracts/OracleConsumer/APITestConsumer.sol).
In this example the oracle address has to be specified in the constructor when deploying the contract.

```solidity
function requestEthereumPrice(address _oracle, string _jobId)
    public
    onlyOwner
  {
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), this, this.fulfillEthereumPrice.selector);
    req.add("get", "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD");
    req.add("path", "USD");
    req.addInt("times", 100);
    sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
  }
```


## 5. Create a request to your node
To fulfill a chainlink request you have to fund your oracle consumer address with some LINK tokens. 

When you call the `requestEthereumPrice(address _oracle, string _jobId)` function you have to specify the oracle address and the JobID from above.
Then the the oracle will be called from the smart contract and send one LINK to the oracle address.

The oracle contract submites an event with the JobID. Because our chainlink node is listening to the oracle events and the JobID the chainlink request will be fullfilled.

## 6. Read the chainlink response
When calling the `currentPrice` function, after the chainlink request was fulfilled the current Ethereum price will be returned.
