import { useContractReader, useBalance } from "eth-hooks";
import { useEventListener } from "eth-hooks/events/useEventListener";
import { ethers } from "ethers";
import { Transactor } from "../helpers";
import { useState } from "react";
import { Input, List, Divider, Card } from "antd";
import { Address, Balance, TokenBalance } from "../components";
import { getRPCPollTime } from "../helpers";
import externalContracts from "../contracts/external_contracts";
const { Search } = Input;

function Home({ localProvider, readContracts, writeContracts, userSigner, gasPrice, address, localChainId }) {
  const localProviderPollingTime = getRPCPollTime(localProvider);
  console.log("contract", readContracts);
  const [unStakeLoading, setUnStakeLoading] = useState(false);
  const [stakeLoading, setStakeLoading] = useState(false);
  const validators = useContractReader(readContracts, "StakingPool", "getValidators");
  const sharePrice = useContractReader(readContracts, "SSVETHCONTRACT", "sharePrice");
  const beaconRewards = useContractReader(readContracts, "StakingPool", "beaconRewards");
  const executionRewards = useContractReader(readContracts, "StakingPool", "executionRewards");
  console.log("sharePrice", sharePrice?.toString());
  //const parsedSharePrice = Number(sharePrice / 10 ** 18).toFixed(18);
  const userEarnings = useContractReader(readContracts, "SSVETHCONTRACT", "balanceOf", [address]);
  console.log("userEarnings", userEarnings?.toString());
  const balanceStaked = useContractReader(readContracts, "StakingPool", "getUserStake", [address]);
  const stakingPoolAddress = readContracts && readContracts?.StakingPool?.address;
  const stakingPoolBalance = useBalance(localProvider, stakingPoolAddress, localProviderPollingTime);
  const ssvEthAllowance = useContractReader(readContracts, "SSVETHCONTRACT", "allowance", [
    address,
    stakingPoolAddress,
  ]);
  const totalSupply = useContractReader(readContracts, "SSVETHCONTRACT", "totalSupply");
  // ** 📟 Listen for broadcast events
  const stakeEvents = useEventListener(readContracts, "StakingPool", "UserStaked", localProvider, 5);

  // The transactor wraps transactions and provides notificiations
  const tx = Transactor(userSigner, gasPrice);

  const handleOnStake = async value => {
    setStakeLoading(true);
    await tx(writeContracts.StakingPool.stake({ value: ethers.utils.parseEther(value) }));
    setStakeLoading(false);
  };

  const handleOnUnstake = async value => {
    if (Number(ethers.utils.parseEther(value)) > balanceStaked) {
      alert("You can't unstake more than you have !");
      return;
    } else {
      setUnStakeLoading(true);
      if (Number(ssvEthAllowance) > 0) {
        await tx(writeContracts.StakingPool.unStake(ethers.utils.parseEther(value)));
      } else {
        //approving max before calling the unstake method
        await tx(
          writeContracts.SSVETHCONTRACT.approve(stakingPoolAddress, "10000000000000000000000000000000000000000"),
        );
        tx(writeContracts.StakingPool.unStake(ethers.utils.parseEther(value)));
      }
    }
    setUnStakeLoading(false);
  };

  return (
    <div>
      <div
        style={{
          border: "1px solid #cccccc",
          width: 600,
          margin: "auto",
          justifyContent: "center",
          marginTop: 32,
          padding: 32,
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
            <h4>ETH/ssvETH ratio:</h4>
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

      <div style={{ border: "1px solid #cccccc", padding: 16, width: 600, margin: "auto", marginTop: 32 }}>
        <h2>Pool overview:</h2>
        <h4>
          Stake your ETH in the staking pool to earn our liquid staked derivative token called ssvETH, which you can
          also use in other DeFi protocols{" "}
        </h4>
        You can find more details{" "}
        <a href="https://github.com/bloxapp/awesome-ssv/blob/main/README.md" target="_blank" rel="noopener noreferrer">
          📕 here
        </a>
        <Divider />
        <div>
          <h4>ssvETH Total Supply: </h4>
          <TokenBalance balance={Number(totalSupply)} fontSize={64} />
        </div>
        <Divider />
        <Card>
          <h3 style={{ paddingTop: 16 }}>ETH under management:</h3>
          <div style={{ display: "flex", justifyContent: "space-around" }}>
            <div>
              <h4 style={{ padding: 8 }}>Active validators:</h4>
              {validators !== undefined ? (
                <div style={{ fontSize: 20 }}>{validators?.length}</div>
              ) : (
                <div style={{ fontSize: 20 }}>0</div>
              )}
            </div>
            <div>
              <h4 style={{ padding: 8 }}>Active stake:</h4>
              <TokenBalance balance={Number(stakingPoolBalance)} fontSize={64} />{" "}
              <span style={{ fontSize: 20, verticalAlign: "middle" }}>ETH</span>
            </div>
            <div>
              <h4 style={{ padding: 8 }}>Rewards:</h4>
              Execution layer rewards :{" "}
              <div style={{ padding: 8, fontSize: 20 }}>
                {" "}
                <TokenBalance balance={Number(beaconRewards)} fontSize={64} />{" "}
                <span style={{ fontSize: 20, verticalAlign: "middle" }}>ETH</span>
              </div>
              Beacon chain rewards :
              <div style={{ padding: 8, fontSize: 20 }}>
                <TokenBalance balance={executionRewards} fontSize={64} />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div
        style={{
          border: "1px solid #cccccc",
          margin: "auto",
          justifyContent: "center",
          width: 800,
          marginTop: 32,
          textAlign: "center",
        }}
      >
        <h2 style={{ paddingTop: 16 }}>Contracts:</h2>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <div style={{ padding: 14 }}>
            <h4 style={{ whiteSpace: "nowrap" }}>SSVETH Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVETHCONTRACT && readContracts.SSVETHCONTRACT.address}
              fontSize={16}
            />
            <p style={{ maxWidth: "350px", textAlign: "left", padding: "8px" }}>
              The SSV decentralized staking system uses The "ssvETH" LSD (liquid staking derivate) token which
              represents user’s stake plus rewards. It is minted upon deposit and burned upon withdrawal.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4 style={{ whiteSpace: "nowrap" }}>Staking Pool Contract: </h4>
            <Address
              value={readContracts && readContracts.StakingPool && readContracts.StakingPool.address}
              fontSize={16}
            />
            <p style={{ maxWidth: "350px", textAlign: "left", padding: "8px" }}>
              The staking pool contract manages deposited funds. It has two main functions, running a validator and
              keeping track of users' rewards. 1. It deposits new validators to the Beacon chain deposit contract (for
              validator activation), and registers validator key shares to SSV Network Contract in order to perform
              validator duties. 2. It keep track of the received rewards by updating ssvETH value and let’s anyone exit
              staking by simply depositing ssvETH to the pool.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4 style={{ whiteSpace: "nowrap" }}>Deposit Contract:</h4>
            <Address
              value={readContracts && readContracts.DEPOSITCONTRACT && readContracts.DEPOSITCONTRACT.address}
              fontSize={16}
            />
            <p style={{ maxWidth: "350px", textAlign: "left", padding: "8px" }}>
              This is the “official” Ethereum Beacon Chain Deposit Contract(see documentation) through which validators
              are registered to the Beacon chain. To join Etherum validator network stakingPool needs to interact with
              this contract, Depositing 32 ETH, specifying staker, validator, stake amount and withdrawal credentials.
            </p>
          </div>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <div style={{ padding: 14 }}>
            <h4 style={{ whiteSpace: "nowrap" }}>SSV Network Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVNETWORKCONTRACT && readContracts.SSVNETWORKCONTRACT.address}
              fontSize={16}
            />
            <p style={{ maxWidth: "350px", textAlign: "left", padding: "8px" }}>
              The core SSV Network contract for performing validator duties (running validator).(see documentation) This
              contract let's anyone register their validator with the SSV network. Operators specified in the
              registerValidator() function, will then observe the contract, see the new validator shares and start
              operating (attesting, proposing) on stakingPool's behalf.
            </p>
          </div>
          <div style={{ padding: 14 }}>
            <h4 style={{ whiteSpace: "nowrap" }}>SSV Token Contract:</h4>
            <Address
              value={readContracts && readContracts.SSVTOKENADDRESS && readContracts.SSVTOKENADDRESS.address}
              fontSize={16}
            />
            <p style={{ maxWidth: "350px", textAlign: "left", padding: "8px" }}>
              The native token of ssv.network used for payments. Staker (Staking Pool) needs to keep balance of this
              token in SSV network contract to be able to pay for the validating services performed by the network
              operators.
            </p>
          </div>
        </div>
      </div>

      <div style={{ width: 500, margin: "auto", marginTop: 32 }}>
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
