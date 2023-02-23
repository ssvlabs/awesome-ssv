// MY INFURA_ID, SWAP IN YOURS FROM https://infura.io/dashboard/ethereum
export const INFURA_ID = process.env.REACT_APP_INFURA_KEY ?? "460f40a260564ac4a4f4b3fffb032dad";
// My Alchemy Key, swap in yours from https://dashboard.alchemyapi.io/
export const ALCHEMY_KEY = process.env.REACT_APP_ALCHEMY_KEY ?? "oKxs-03sij-U_N0iOlrSsZFr29-IqbuF";

// MY ETHERSCAN_ID, SWAP IN YOURS FROM https://etherscan.io/myapikey
export const ETHERSCAN_KEY = process.env.REACT_APP_ETHERSCAN_API_KEY ?? "DNXJA8RX2Q3VZ4URQIWP7Z68CJXQZSC6AW";

// BLOCKNATIVE ID FOR Notify.js:
export const BLOCKNATIVE_DAPPID = process.env.REACT_APP_BLOCKNATIVE_DAPP_ID ?? "0b58206a-f3c0-4701-a62f-73c7243e8c77";

// Docker Hardhat Host
export const HARDHAT_HOST = process.env.REACT_APP_HARDHAT_HOST ?? "http://localhost";

/*
Decrease the number of RPC calls by passing this value to hooks
with pollTime (useContractReader, useBalance, etc.).
Set it to 0 to disable it and make RPC calls "onBlock".
Note: this is not used when you are in the local hardhat chain.
*/
export const RPC_POLL_TIME = 30000;

const localRpcUrl = process.env.REACT_APP_CODESPACES
  ? `https://${window.location.hostname.replace("3000", "8545")}`
  : "http://" + (global.window ? window.location.hostname : "localhost") + ":8545";

export const NETWORKS = {
  localhost: {
    name: "localhost",
    color: "#666666",
    chainId: 31337,
    blockExplorer: "",
    rpcUrl: localRpcUrl,
  },

  goerli: {
    name: "goerli",
    color: "#0975F6",
    chainId: 5,
    faucet: "https://goerli-faucet.slock.it/",
    blockExplorer: "https://goerli.etherscan.io/",
    rpcUrl: `https://goerli.infura.io/v3/${INFURA_ID}`,
  },
 

};

export const NETWORK = chainId => {
  for (const n in NETWORKS) {
    if (NETWORKS[n].chainId === chainId) {
      return NETWORKS[n];
    }
  }
};
