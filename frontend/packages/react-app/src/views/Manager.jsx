import { List, Typography, Input } from "antd";
import { useContractReader } from "eth-hooks";
import { useEventListener } from "eth-hooks/events/useEventListener";
import { Address, Balance } from "../components";
import { ethers } from "ethers";
const { Search } = Input;
export default function Manager({ localProvider, tx, writeContracts, readContracts }) {
  const operators = useContractReader(readContracts, "STAKINGPOOL", "getOperators");
  const pubKeyEvents = useEventListener(readContracts, "STAKINGPOOL", "PubKeyDeposited", localProvider, 5);
  console.log("operators", operators);
  const data = ["0x0000536dbD99d918092249Ef4eDe4a69A35CccCa"];
  const handleOnSetNewOperators = async value => {
    await tx(writeContracts.STAKINGPOOL.setOperators(JSON.parse(value)));
  };

  const handleUpdateNewSharePrice = async value => {
    await tx(writeContracts.STAKINGPOOL.updateSharePrice(ethers.utils.parseEther(value.toString()).toString()));
  };
  return (
    <div>
      <div style={{ padding: 16, width: 400, margin: "auto", marginTop: 32 }}>
        <h2>Manager View</h2>
      </div>

      <div style={{ width: 600, margin: "auto", marginTop: 32 }}>
        <List
          header={<div>All Validators</div>}
          bordered
          dataSource={data}
          renderItem={item => (
            <List.Item>
              <Typography.Text mark>[Validator 1]</Typography.Text> {item}
            </List.Item>
          )}
        />
      </div>
      <div style={{ display: "flex", justifyContent: "center", margin: "auto", marginTop: 32 }}>
        <List
          size="small"
          header={<div>All Operators</div>}
          bordered
          dataSource={operators}
          renderItem={item => <List.Item>{item}</List.Item>}
        />
        <div style={{ marginInline: "50px" }}>
          <div style={{ padding: 8 }}>Set new operators:</div>
          <Search
            style={{ margin: "auto" }}
            placeholder="new operators Ids array e.g: [1,2,3,4]"
            enterButton="Submit"
            size="medium"
            onSearch={value => handleOnSetNewOperators(value)}
          />

          <div style={{ padding: 8, marginTop: 12 }}>Update share price:</div>
          <Search
            style={{ margin: "auto" }}
            placeholder="new share price value"
            enterButton="Submit"
            size="medium"
            onSearch={value => handleUpdateNewSharePrice(value)}
          />
        </div>
      </div>
      <div style={{ width: 500, margin: "auto", marginTop: 32 }}>
        <div>Public Key Deposited Events:</div>
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
    </div>
  );
}
