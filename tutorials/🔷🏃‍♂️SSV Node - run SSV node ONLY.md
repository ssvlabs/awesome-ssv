# 🔷🏃‍♂️SSV Node - run SSV node Only

[![Video walkthrough & launchig 🌈LSD pool](http://img.youtube.com/vi/4_Ek8mCUZCk/0.jpg)](http://www.youtube.com/watch?v=4_Ek8mCUZCk "🔷🏃‍♂️SSV Node - run SSV node ONLY")

**DISCLAIMER**
The content provided is for informational purposes only and should not be considered as professional advice. The information presented may not be complete, accurate or up-to-date. The reader or viewer is solely responsible for any actions taken based on the information provided. The author and publisher shall not be held liable for any losses, damages or injuries arising from the use of the information provided. It is recommended to seek professional advice for specific situations.

## Prerequistes

- Execution client and Beacon node
- `docker` installed

  
This tutorial assumes you already have Execution client and Beacon node running (step one) and `docker` installed. If this is not the case, there are many tutorials how to just run nodes with exposed ports, see [my other ssv tutorial](https://github.com/bloxapp/awesome-ssv/blob/main/tutorials/Run%20SSV%20node%20in%2010%20minutes%20by%20markoInEther%20server%20setup%20eth-docker%20validator%20registration.md) running full stack using `eth-docker`. 


## Steps 

To run an ssv nodes go through these 3 steps: 
1. ~~running Execution Node and Beacon node with exposed ws port(EN) and http port(BN).~~
2. creating configuration file for your ssv node.
3. running ssv node container.



*Once you are finished with step one, continue with this tutorial.* 

### Creating configuration file

##### Generate Operator key pair

run: 
```bash
docker run -d --name=ssv_node_op_key -it 'bloxstaking/ssv-node:latest' \
/go/bin/ssvnode generate-operator-keys && docker logs ssv_node_op_key --follow \
&& docker stop ssv_node_op_key && docker rm ssv_node_op_key
```


You will get output similar to this one: 
```bash 
2023-03-31T11:36:02.885763Z     INFO    SSV-Node        cli/generate_operator_keys.go:27        generated public key (base64) {"pk": "LS0tLS1CRUd........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................S0K"}

2023-03-31T11:36:02.885881Z     INFO    SSV-Node        cli/generate_operator_keys.go:28        generated private key (base64)        {"sk": "LS0t................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................tLQo="}
```

save both public key `"pk"` and private (secret) key `"sk"`  into secure location, you will need them both later. 

**Important**
Do **NOT** forget to include `...==` at the end of the Secret Key if it is part of the key. 

-------------------------------- 

#### Create config.yaml

create new folder where you will store your ssv node config file: 

`mkdir my-ssv-node && cd my-ssv-node`

create config file:

`sudo nano config.yaml`

#### config.yaml - edit this 

```
db:
  Path: /tmp/ssv-db
  Type: badger-db
p2p:
  DiscoveryType: discv5
  TcpPort: 13001
  UdpPort: 12001
eth2:
  BeaconNodeAddr: http://<your beacon node ip>:5052
  Network: prater
eth1:
  ETH1Addr: ws://<your execution layer web socket address>:8546
OperatorPrivateKey: <your private key>
MetricsAPIPort: 15000
global:
  LogFormat: json
  LogLevelFormat: lowercase
  LogLevel: info
  
  ```




update your config file: 

`TcpPort: 13001`
`UdpPort: 12001`

These are the default ports used to communicate with other ssv nodes. You can leave them as is, make sure they are free and do **NOT** put in your execution or beacon chain node address. 

`BeaconNodeAddr: http://<your beacon node ip>:5052`

Change to your beacon node address, change the port if you are not using the default one. 

`ETH1Addr: ws://<your execution layer web socket address>:8546`

Change to your execution node web socket address, change the port if you are not using the default one.

`OperatorPrivateKey: <your private key>


Insert your Operator secret key `"sk"`, do **NOT** forget to include `...==` at the end of the Secret Key if it is part of the key. 


`MetricsAPIPort: 15000`

You can leave it as is

#### config.yaml - example 
After you fill in everything your config should looks something like this: 

```
db:
  Path: /tmp/ssv-db
  Type: badger-db
p2p:
  DiscoveryType: discv5
  TcpPort: 13001
  UdpPort: 12001
eth2:
  BeaconNodeAddr: http://consensus:5052
  Network: prater
eth1:
  ETH1Addr: ws://execution:8546
OperatorPrivateKey: LS0tLS1CR............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................WQVRFIEtFWS0tLS0tCg==
MetricsAPIPort: 15000
global:
  LogFormat: json
  LogLevelFormat: lowercase
  LogLevel: info
  
  ```


-------------------------------- 



### Running ssv node

go to your folder with your `config.yaml` file: 

`cd my-ssv-node`



#### commands - edit this 

```bash
# open ports 
sudo ufw allow 13001/tcp
sudo ufw allow 12001/udp

# running container 
docker run -d --restart unless-stopped --name=`<your container name>`  -e \
CONFIG_PATH=./config.yaml -p 13001:13001 -p 12001:12001/udp -v \
$(pwd)/config.yaml:/config.yaml -v $(pwd):/data -it \
--network eth-docker_default \
'bloxstaking/ssv-node:latest' make BUILD_PATH=/go/bin/ssvnode start-node


# update container version
docker rm -f -v my-ssv-node && docker pull bloxstaking/ssv-node:latest

# check logs 
docker logs my-ssv-node --follow --tail 50


```


check your docker network name: 

`docker network ls`

1. Edit name of your container 
	1. e.g. `<your container name>` -> `my-ssv-node`
2. Edit name of your docker network 
	1. e.g. `<your docker network>` -> `eth-docker_default`
3. Edit ssv ports if you use different than defaults 
	1. e.g. `<your container name>` -> `my-ssv-node`


#### commands - example

```bash
# open ports 
sudo ufw allow 13003/tcp
sudo ufw allow 12003/udp

# running container 
docker run -d --restart unless-stopped --name=my-ssv-node -e \
CONFIG_PATH=./config.yaml -p 13003:13003 -p 12003:12003/udp -v \
$(pwd)/config.yaml:/config.yaml -v $(pwd):/data -it \
--network eth-docker_default \
'bloxstaking/ssv-node:latest' make BUILD_PATH=/go/bin/ssvnode start-node


# update container version
docker rm -f -v my-ssv-node && docker pull bloxstaking/ssv-node:latest

# check logs 
docker logs my-ssv-node --follow --tail 50


```
