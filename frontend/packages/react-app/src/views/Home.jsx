import { useContractReader } from "eth-hooks";
import { useEventListener } from "eth-hooks/events/useEventListener";
import { ethers } from "ethers";
import { Transactor } from "../helpers";
import { useState } from "react";
import { Input, List } from "antd";
import { Address, Balance, TokenBalance } from "../components";
import externalContracts from "../contracts/external_contracts";
const { Search } = Input;

function Home({ localProvider, readContracts, writeContracts, userSigner, gasPrice, address }) {
  const [unStakeLoading, setUnStakeLoading] = useState(false);
  const [stakeLoading, setStakeLoading] = useState(false);

  const sharePrice = useContractReader(readContracts, "SSVETHCONTRACT", "sharePrice");
  const parsedSharePrice = Number(sharePrice / 10 ** 18);
  const balanceStaked = useContractReader(readContracts, "SSVETHCONTRACT", "balanceOf", [address]);
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
    setUnStakeLoading(true);
    if (Number(ssvEthAllowance) > 0) {
      await tx(writeContracts.STAKINGPOOL.unStake(ethers.utils.parseEther(value)));
    } else {
      //approving max before calling the unstake method
      await tx(writeContracts.SSVETHCONTRACT.approve(stakingPoolAddress, "10000000000000000000000000000000000000000"));
      tx(writeContracts.STAKINGPOOL.unStake(ethers.utils.parseEther(value)));
    }
    setUnStakeLoading(false);
  };

  console.log("💸 balanceStaked:", balanceStaked);
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center", pmarginTop: 32 }}>
        <div style={{ padding: 8 }}>
          <div>Staking Pool Contract:</div>
          <Address value={readContracts && readContracts.STAKINGPOOL && readContracts.STAKINGPOOL.address} />
        </div>
        <div style={{ padding: 8 }}>
          <div>SSVETH Contract:</div>
          <Address value={readContracts && readContracts.SSVETHCONTRACT && readContracts.SSVETHCONTRACT.address} />
        </div>
        <div style={{ padding: 8 }}>
          <div>Deposit Contract:</div>
          <Address value={readContracts && readContracts.DEPOSITCONTRACT && readContracts.DEPOSITCONTRACT.address} />
        </div>
        <div style={{ padding: 8 }}>
          <div>SSV Network Contract:</div>
          <Address
            value={readContracts && readContracts.SSVNETWORKCONTRACT && readContracts.SSVNETWORKCONTRACT.address}
          />
        </div>
        <div style={{ padding: 8 }}>
          <div>SSV Token Contract:</div>
          <Address value={readContracts && readContracts.SSVTOKENADDRESS && readContracts.SSVTOKENADDRESS.address} />
        </div>
      </div>
      <div style={{ display: "flex", justifyContent: "center", padding: 12 }}>
        <div style={{ padding: 8 }}>
          <div>ssvETH Total Supply: </div>
          <TokenBalance balance={Number(totalSupply)} fontSize={64} />
        </div>
        <div style={{ padding: 8 }}>
          <div>ssvETH Price: </div>
          <TokenBalance balance={Number(0)} price={0} fontSize={64} />
        </div>
      </div>
      <div style={{ display: "flex", justifyContent: "center", padding: 12 }}>
        <div style={{ padding: 8 }}>
          <div>You staked: </div>
          <TokenBalance balance={Number(balanceStaked)} fontSize={64} />
        </div>

        <div style={{ padding: 8 }}>
          <div>ssvETH Rewards:</div>
          <TokenBalance balance={Number(balanceStaked * parsedSharePrice)} fontSize={64} />
        </div>

        <div style={{ padding: 8 }}>
          <div>Share price:</div>
          <Balance balance={sharePrice} fontSize={64} />
        </div>
      </div>
      <div style={{ margin: 16 }}>
        <Search
          style={{ margin: "auto", width: "30%" }}
          placeholder="input unstake amount"
          enterButton="Unstake 🦴"
          size="large"
          loading={unStakeLoading}
          onSearch={value => handleOnUnstake(value)}
        />
      </div>

      <div style={{ margin: 16 }}>
        <Search
          style={{ margin: "auto", width: "30%" }}
          placeholder="input stake amount"
          enterButton="Stake 🥩"
          size="large"
          loading={stakeLoading}
          onSearch={value => handleOnStake(value)}
        />
      </div>

      <div style={{ width: 500, margin: "auto", marginTop: 32 }}>
        <div>Stake Events:</div>
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
