FROM golang:1.16.0

WORKDIR /go/src/github.com/

# Use third-party sources mirror
RUN apt-get update && apt-get install -y ca-certificates

RUN wget https://github.com/Fantom-foundation/go-lachesis/archive/v0.8.0-rc.2.tar.gz -P /go/src/github.com/ \
  && cd /go/src/github.com/ \
  && tar -xvf v0.8.0-rc.2.tar.gz \
  && rm -rf v0.8.0-rc.2.tar.gz \
  && cd go-lachesis-0.8.0-rc.2 && make

RUN pwd
RUN ls -la
RUN ls -la /go/src/github.com/

CMD /go/src/github.com/go-lachesis-0.8.0-rc.2/build/lachesis --fakenet 1/1 --rpc --rpcaddr=0.0.0.0 --rpcport=3001  --rpcapi=eth,net,web3,debug,ftm,sfc --ws --wsaddr=0.0.0.0 --wsport=8535 --wsapi=eth,net,web3,debug,ftm,sfc --port 5050