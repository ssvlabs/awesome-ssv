import { List, Typography, Input, Divider, Form, Button } from "antd";
import { useContractReader } from "eth-hooks";
import { useEventListener } from "eth-hooks/events/useEventListener";
import { Address, Balance } from "../components";
import { ethers } from "ethers";

const { Search } = Input;

export default function Manager({ localProvider, tx, writeContracts, readContracts }) {
  const operators = useContractReader(readContracts, "StakingPool", "getOperators");
  const pubKeyEvents = useEventListener(readContracts, "StakingPool", "PubKeyDeposited", localProvider, 5);
  const KeySharesDepositedEvents = useEventListener(readContracts, "StakingPool", "KeySharesDeposited", localProvider, 5);

  const validators = useContractReader(readContracts, "StakingPool", "getValidators");

  console.log("all validators", validators)

  const handleOnSetNewOperators = async value => {
    await tx(writeContracts.StakingPool.updateOperators(JSON.parse(value)));
  };

  const handleUpdateBeaconRewards = async value => {
    await tx(writeContracts.StakingPool.updateBeaconRewards(ethers.utils.parseEther(value.toString()).toString()));
  };

  const handleOnSetNewShareprice = async value => {
    await tx(writeContracts.StakingPool.updateSharePrice(ethers.utils.parseEther(value.toString()).toString()));
  };


  return (
    <div>
      <div style={{ border: "1px solid #cccccc", width: 650, margin: "auto", marginTop: 32 }}>
        <h2 style={{ paddingTop: 16 }}>Pool managed overview:</h2>

        <div style={{ display: "flex" }}>
          <List
            style={{ width: "65%", margin: "auto", marginBlock: 32 }}
            header={<h4>All Pool managed validators</h4>}
            bordered
            dataSource={validators}
            renderItem={item => (
              <>
                <List.Item>
                  <Typography.Text style={{ maxWidth: "100%" }} mark>{item}</Typography.Text>
                </List.Item>
                <br></br>
              </>
            )}
          />
          <List
            style={{ width: "25%", margin: "auto", marginBlock: 32 }}
            size="small"
            header={<h4>All Operators</h4>}
            bordered
            dataSource={operators}
            renderItem={item => <List.Item>{item}</List.Item>}
          />
        </div>
      </div>
      <div
        style={{
          border: "1px solid #cccccc",
          width: 600,
          justifyContent: "center",
          margin: "auto",
          marginTop: 32,
          padding: 16,
        }}
      >
        <h2>Manager actions:</h2>
        <div style={{ marginInline: "50px" }}>
          <h4 style={{ padding: 8 }}>Set new operators: {"(e.g: [1, 2, 3, 4])"}</h4>
          <Search
            style={{ width: "70%", margin: "auto" }}
            placeholder="new operators Ids array"
            enterButton="Submit"
            size="medium"
            onSearch={value => handleOnSetNewOperators(value)}
          />
          <Divider />
          <h4 style={{ padding: 8, marginTop: 12 }}>Update Beacon chain rewards:</h4>
          <Search
            style={{ width: "70%", margin: "auto" }}
            placeholder="new Beacon chain rewards value"
            enterButton="Submit"
            size="medium"
            onSearch={value => handleUpdateBeaconRewards(value)}
          />
          <Divider />
          {/* <h4 style={{ padding: 8, marginTop: 12 }}>Update share price:</h4>
          <Search
            style={{ width: "70%", margin: "auto" }}
            placeholder="new share price value"
            enterButton="Submit"
            size="medium"
            onSearch={value => handleOnSetNewShareprice(value)}
          />
          <Divider /> */}
        </div>
      </div>

      <div style={{ width: 600, margin: "auto", marginTop: 32, display: "flex" }} >
        <div style={{ width: 300, margin: "auto" }}>
          <h3 style={{ paddingTop: 16 }}>Public Key Deposited Events:</h3>
          <List
            dataSource={pubKeyEvents}
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

        <div style={{ width: 300, margin: "auto" }}>
          <h3 style={{ paddingTop: 16 }}>Key Shares Deposited Events:</h3>
          <List
            dataSource={KeySharesDepositedEvents}
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
    </div >
  );
}
