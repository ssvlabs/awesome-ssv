import { useContractReader } from "eth-hooks";
import { useEventListener } from "eth-hooks/events/useEventListener";
import { ethers } from "ethers";
import { Transactor } from "../helpers";
import { useState } from "react";
import { Input, List, Divider } from "antd";
import { Address, Balance, TokenBalance } from "../components";
import externalContracts from "../contracts/external_contracts";
const { Search } = Input;

function Home({ localProvider, readContracts, writeContracts, userSigner, gasPrice, address }) {
  const [unStakeLoading, setUnStakeLoading] = useState(false);
  const [stakeLoading, setStakeLoading] = useState(false);

  const sharePrice = useContractReader(readContracts, "SSVETHCONTRACT", "sharePrice");
  console.log("sharePrice", sharePrice?.toString());
  //const parsedSharePrice = Number(sharePrice / 10 ** 18).toFixed(18);
  const userEarnings = useContractReader(readContracts, "SSVETHCONTRACT", "balanceOf", [address]);
  console.log("userEarnings", userEarnings?.toString());
  const balanceStaked = useContractReader(readContracts, "STAKINGPOOL", "getUserStake", [address]);
  const stakingPoolAddress = externalContracts[5].contracts.STAKINGPOOL.address;
  const ssvEthAllowance = useContractReader(readContracts, "SSVETHCONTRACT", "allowance", [
    address,
    stakingPoolAddress,
  ]);
  const totalSupply = useContractReader(readContracts, "SSVETHCONTRACT", "totalSupply");
  // ** 📟 Listen for broadcast events
  const stakeEvents = useEventListener(readContracts, "STAKINGPOOL", "UserStaked", localProvider, 5);

  // The transactor wraps transactions and provides notificiations
  const tx = Transactor(userSigner, gasPrice);

  const handleOnStake = async value => {
    setStakeLoading(true);
    await tx(writeContracts.STAKINGPOOL.stake({ value: ethers.utils.parseEther(value) }));
    setStakeLoading(false);
  };

  const handleOnUnstake = async value => {
    if (ethers.utils.parseEther(value) > balanceStaked) {
      alert("You can't unstake more than you have !");
      return;
    } else {
      setUnStakeLoading(true);
      if (Number(ssvEthAllowance) > 0) {
        await tx(writeContracts.STAKINGPOOL.unStake(ethers.utils.parseEther(value)));
      } else {
        //approving max before calling the unstake method
        await tx(
          writeContracts.SSVETHCONTRACT.approve(stakingPoolAddress, "10000000000000000000000000000000000000000"),
        );
        tx(writeContracts.STAKINGPOOL.unStake(ethers.utils.parseEther(value)));
      }
    }
    setUnStakeLoading(false);
  };

  return (
    <div>
      <div style={{ border: "1px solid #cccccc", padding: 16, width: 400, margin: "auto", marginTop: 32 }}>
        <h1>Pool overview:</h1>
        <h4>Stake your ETH to earn ssvETH !</h4>
        You can find more details{" "}
        <a href="https://github.com/bloxapp/awesome-ssv/blob/main/README.md" target="_blank" rel="noopener noreferrer">
          📕 here
        </a>
        <Divider />
        <h4>Staking Pool Contract: </h4>
        <Address
          value={readContracts && readContracts.STAKINGPOOL && readContracts.STAKINGPOOL.address}
          fontSize={16}
        />
        <p style={{ textAlign: "center", padding: "8px" }}>
          The staking pool contract that allows users to deposit ETH and receive rewards in ssvETH. The manager can also
          launch and manage validators using it.
        </p>
        <Divider />
        <h4>ssvETH Total Supply: </h4>
        <TokenBalance balance={Number(totalSupply)} fontSize={64} />
      </div>
      <div
        style={{
          border: "1px solid #cccccc",
          margin: "auto",
          justifyContent: "center",
          width: 750,
          marginTop: 32,
          textAlign: "center",
        }}
      >
        <h2 style={{ paddingTop: 16 }}>Contracts:</h2>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <div style={{ padding: 14 }}>
            <h4>SSVETH Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVETHCONTRACT && readContracts.SSVETHCONTRACT.address}
              fontSize={16}
            />
            <p style={{ textAlign: "left", padding: "8px" }}>
              The SSV decentralized staking system uses The "ssvETH" token to reward the stakers. Its contract also
              allows the manager change the share price.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4>Deposit Contract:</h4>
            <Address
              value={readContracts && readContracts.DEPOSITCONTRACT && readContracts.DEPOSITCONTRACT.address}
              fontSize={16}
            />
            <p style={{ textAlign: "left", padding: "8px" }}>
              This deposit contract is used to create and store deposits. It also allows for checking the deposit root
              and count.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4>SSV Network Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVNETWORKCONTRACT && readContracts.SSVNETWORKCONTRACT.address}
              fontSize={16}
            />
            <p style={{ textAlign: "left", padding: "8px" }}>
              The CORE SSV Network environment contract, including the SSV Network token and the SSV Network registry.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4>SSV Token Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVTOKENADDRESS && readContracts.SSVTOKENADDRESS.address}
              fontSize={16}
            />
            <p style={{ textAlign: "left", padding: "8px" }}>
              The native token of ssv.network, Secret Shared Validator ($SSV). Its main use cases are payments and
              governance.
            </p>
          </div>
        </div>
      </div>
      <div
        style={{
          border: "1px solid #cccccc",
          width: 450,
          margin: "auto",
          justifyContent: "center",
          marginTop: 32,
          padding: 16,
        }}
      >
        <h2>Your Stake:</h2>
        <div
          style={{
            display: "flex",
            margin: "auto",
            justifyContent: "center",
          }}
        >
          <div style={{ padding: 8 }}>
            <h4>Your ETH staked: </h4>
            <TokenBalance balance={Number(balanceStaked)} fontSize={64} />
          </div>

          <div style={{ padding: 8 }}>
            <h4>Your ssvETH:</h4>
            <TokenBalance balance={Number(balanceStaked * (sharePrice / 10 ** 18))} fontSize={64} />
          </div>

          <div style={{ padding: 8 }}>
            <h4>Share price:</h4>
            <TokenBalance balance={sharePrice} fontSize={64} />
          </div>
        </div>
        <div style={{ margin: 16 }}>
          <Search
            style={{ margin: "auto", width: "80%" }}
            placeholder="input unstake amount"
            enterButton="Unstake 🦴"
            size="medium"
            loading={unStakeLoading}
            onSearch={value => handleOnUnstake(value)}
          />
        </div>
        <div style={{ margin: 16 }}>
          <Search
            style={{ margin: "auto", width: "80%" }}
            placeholder="input stake amount"
            enterButton="Stake 🥩"
            size="medium"
            loading={stakeLoading}
            onSearch={value => handleOnStake(value)}
          />
        </div>
      </div>
      <div style={{ border: "1px solid #cccccc", width: 500, margin: "auto", marginTop: 32 }}>
        <h2 style={{ paddingTop: 16 }}>Stake Events:</h2>
        <List
          dataSource={stakeEvents}
          renderItem={item => {
            return (
              <List.Item key={item.blockNumber}>
                <Address value={item.args[0]} fontSize={16} /> =>
                <Balance balance={item.args[1]} />
              </List.Item>
            );
          }}
        />
      </div>
    </div>
  );
}

export default Home;
