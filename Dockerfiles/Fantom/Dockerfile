FROM golang:1.16.0

WORKDIR /go/src/github.com/

# Use third-party sources mirror
RUN apt-get update && apt-get install -y ca-certificates

RUN git clone https://github.com/Fantom-foundation/go-lachesis.git \
    && cd go-lachesis \
    && git checkout develop2 \
    && go build -o ./build/lachesis ./cmd/lachesis

RUN mkdir lachesis-data

CMD /go/src/github.com/go-lachesis/build/lachesis --nousb --fakenet 1/1 --rpc --rpcaddr=0.0.0.0 --rpcport=3001  --rpcapi=eth,net,web3,debug,ftm,sfc --ws --wsaddr=0.0.0.0 --wsport=8546 --wsapi=eth,net,web3,debug,ftm,sfc --port 5050 --datadir ./lachesis-data