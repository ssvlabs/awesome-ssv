## Setting up SSV node

[![🏃‍♂️🦄Eaisiest way to run SSV node in 10 minutes🚀](http://img.youtube.com/vi/HFb4uxHC50w/0.jpg)](https://www.youtube.com/watch?v=HFb4uxHC50w "🏃‍♂️🦄Eaisiest way to run SSV node in 10 minutes🚀")

**DISCLAIMER**
The content provided is for informational purposes only and should not be considered as professional advice. The information presented may not be complete, accurate or up-to-date. The reader or viewer is solely responsible for any actions taken based on the information provided. The author and publisher shall not be held liable for any losses, damages or injuries arising from the use of the information provided. It is recommended to seek professional advice for specific situations.

## Steps

follow along with the video

get linux server setup
Install prerequisites with bash script
(pasted at the end of this description)
Setup eth-docker
Setup ssv node
Generate operator key https://eth-docker.net/Support/BloxSSV
Register operator on goerli

**IMPORTANT**
When you are copying your secret key `SK` it **must** include equal sign `"="` if it is included at the end of your key. In VS code if you double click on the key it will select it without it so be careful. 

**Example**
Generated key pair looks like this: 
```
2023-03-31T11:36:02.885763Z     INFO    SSV-Node        cli/generate_operator_keys.go:27        generated public key (base64) {"pk": "LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBelluYmdsUXk1My8zcHpnWHNJaTAKWmpSekpOUEN0UUdZZXpWVW9PK3g1eTJCMEZGbnd0K1c1RXNNUmFPY3p2ZHBTNnBNd256Um5FOVdxQjVzNDBCOQppRGVjeldGZkt6V3VDRm1yWGtGS2RRVFVmVXdmZmUwQUxmTFo1RHhaUU5XTmZWVnRpZUZ5K3JxTFNDL1V1bGFkCjU5aGQ5RmxWQndLSmFZc1VCVzYzRDBRSEJPZmp6eTRLOEw4eFFOUWRJTWtLUUlpOTNIWEhvQnpjN1U2bUp6cnMKR3JxVmRia0xsem16SHBEdVBLR0lYdnA2NkdyRER5c3F5RmFOQTBjTG14ZEdQMG5EVWxwK0ZsMThWTGduMTRBRQoxQ041WmRUSk5JaEtvVXQ3YjhsSjZ5UUxjaUpIUFZiZUpKZUIxTlNtQyttamJ4Zy9PWXY2S05ZOHQyS1FyV3p0Ckl3SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K"}
2023-03-31T11:36:02.885881Z     INFO    SSV-Node        cli/generate_operator_keys.go:28        generated private key (base64)        {"sk": "LS0tLS1CRUd......................................................................................JVkFURSBLRVktLS0tLQo="}
```


The key you paste into your config file should look like this: 
`LS0tLS1CRUd......................................................................................JVkFURSBLRVktLS0tLQo=`


 
### scripts

create_user.sh

---

```bash
#!/bin/bash

# Prompt for username
read -p "Enter username: " username

# Create user
useradd -m -s /bin/bash "$username"

# Prompt for password
passwd "$username"

# add root
usermod -aG sudo "$username"

# Switch to new user
su "$username"

```

install-main.sh

---

```bash
#!/bin/bash


# Update and upgrade packages
sudo apt update -y && sudo apt upgrade -y

# Install necessary packages
sudo apt install -y build-essential git libssl-dev

# Open ports
# Check if ufw is available
if command -v ufw > /dev/null 2>&1; then
    # Use ufw
    ufw allow 13001/tcp
    ufw allow 13001/udp
    ufw allow 12001/tcp
    ufw allow 12001/udp
    ufw allow 9000/tcp
    ufw allow 9000/udp
    ufw allow 30303/tcp
    ufw allow 30303/udp
else
    # Check if nftables is available
    if command -v nft > /dev/null 2>&1; then
        # Use nftables
        nft add rule inet filter input tcp dport {13001,12001,9001,9000,8545,30303} accept
        nft add rule inet filter input udp dport {13001,12001,9001,9000,8545,30303} accept
    else
        # Use iptables
        iptables -A INPUT -p tcp -m multiport --dports 13001,12001,9001,9000,8545,30303 -j ACCEPT
        iptables -A INPUT -p udp -m multiport --dports 13001,12001,9001,9000,8545,30303 -j ACCEPT
    fi
fi

# Download eth-docker
cd ~ && git clone https://github.com/eth-educators/eth-docker.git && cd eth-docker

# Install pre-requisites such as Docker
./ethd install

# Configure eth-docker - have an Ethereum address handy where you want Execution Layer rewards to go
./ethd config

```

-------------------------------- 

## Registering SSV node to SSV network, migration from v2 to v3

[![🚀🚀🦄 SSV Operator + Validator Migration V2(shifu) to V3(Jato)](http://img.youtube.com/vi/HxLFC7tMYIs/0.jpg)](https://www.youtube.com/watch?v=HxLFC7tMYIs "🚀🚀🦄 SSV Operator + Validator Migration V2 to V3")

## Steps

Follow along with the video, first half will guide you through deregistering operator from v2 network. 
You can skip this part, if you only need to register a new operator to v3. 

[See other tutorials](https://www.youtube.com/channel/UCD7q4qIhrhFjEhSxGdLR-CQ)

## Reach out 

[SSV discord](https://discord.gg/invite/ssvnetworkofficial)
 - `# operators-general` channel 

## Other tutorials 

[markoInEther youtube channel](https://www.youtube.com/channel/UCD7q4qIhrhFjEhSxGdLR-CQ){:target="_blank"}



