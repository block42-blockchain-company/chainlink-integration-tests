# chainlink-integration-tests
Chainlink integration tests for evm compatible blockchains

## Run the integration tests

### Install requirements

```
pip install -r requirements.txt
```

install pytest if not yet installed
```
pip install pytest
```

### private keys
Set the private key of your wallet as environment variable.
```
export PK={private-key}
```

### run the tests

```
pytest tests
```
