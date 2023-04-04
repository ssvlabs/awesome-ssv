## Video

[![🏃‍♂️🦄Eaisiest way to run SSV node in 10 minutes🚀](http://img.youtube.com/vi/HFb4uxHC50w/0.jpg)](https://www.youtube.com/watch?v=HFb4uxHC50w "🏃‍♂️🦄Eaisiest way to run SSV node in 10 minutes🚀"){:target="\_blank"}

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
    ufw allow 9001/tcp
    ufw allow 9001/udp
    ufw allow 9000/tcp
    ufw allow 9000/udp
    ufw allow 8545/tcp
    ufw allow 8545/udp
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