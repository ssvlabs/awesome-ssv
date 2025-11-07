<br/>
<div align="center">
  <img width="250px" src="./awesome_ssv.png">
</div>
<br/>
<div align="center">
An Awesome list of <a href='https://ssv.network/'>SSV</a>-related tools & projects. 
<br />
The goal is to help developers start <a href='https://ssv.network/ba-dev/'>building with SSV</a>. 
<br/>
If you are looking to add your project to this page - head over to <a href='#how-to-contribute'>the Contribute section</a>.
<br/>
</div>

---
## Contents

- [Intro](#introduction)
- [Tools](#tools)
- [Projects Showcase](#projects-showcase)
- [Operator services](#operator-services)
- [Related Concepts](#related-concepts)
- [How to contribute](#how-to-contribute)
- [Add your project](#how-to-add-your-project)
---

## Introduction
SSV is a permissionless network that enables the distribution of validator operations between non-trusting operators. The [SSV Network smart contract](https://docs.ssv.network/developers/smart-contracts/ssvnetwork) allows anyone to integrate with the SSV protocol.

#### Documentation

The best way to start building with SSV Network is by **reading our documentation** at [docs.ssv.network](https://docs.ssv.network/).

#### Connect with teams

The best way to connect is via [Discord channel](https://discord.gg/5vT22pRBrf). There you'll find help from community or SSV team will help to find the right team for your question.

---

## Tools

#### SDK

- [SSV SDK](https://github.com/ssvlabs/ssv-sdk) `GPL | TS` - A powerful library to interact with SSV Network programmatically. See module reference and examples [in our documentation](https://docs.ssv.network/developers/SSV-SDK/).

#### Subgraph

- [SSV Subgraph](https://github.com/ssvlabs/ssv-subgraph) `GPL | TS` - Subgraph that indexed SSV Smart Contract events. Described in details [in our documentation](https://docs.ssv.network/developers/tools/ssv-subgraph/). Our mainnet endpoint is `https://api.studio.thegraph.com/query/71118/ssv-network-ethereum/version/latest`, you can call it using your The Graph API key.

#### Validator key splitting (key shares creation)

- [SSV Keys](https://github.com/ssvlabs/ssv-keys) `GPL | TS` - A tool to split validator key into keyshares for chosen operators. To learn more read [the documentation](https://docs.ssv.network/developers/tools/ssv-key-distributor).

#### Distributed (validator) Key Generation

You can read more about [how DKG works here](https://docs.ssv.network/developers/tools/ssv-dkg-client/).

- [DKG by SSV Labs](https://github.com/ssvlabs/ssv-dkg) `GPL | Go` - Primary DKG tool, used across SSV Network.

#### SSV Node clients

You can read more about how [SSV Operators work here](https://docs.ssv.network/operators/operator-onboarding/).

- [SSV Node by SSV Labs](https://github.com/ssvlabs/ssv) `GPL | Go`
- [SSV Node by Sigma Prime](https://github.com/sigp/anchor) `Apache | Rust`

---

## Projects Showcase

- [FRENS](https://github.com/frens-pool) `Solidity/TS` - A tool to create own staking pools. The creation is done with smart contracts, validators are managed by SSV operators.
- [MonitorSSV](https://github.com/monitorssv/monitorssv) `MIT | Go/JS` - SSV Network monitoring tool with various cool features.
- [Verify Keyshares](https://github.com/RaekwonIII/verify-keyshares) `TS` - Simple app to verify that generated keyshares are valid.
- [Cluster Balance Tool](https://github.com/taylorferran/cluster-balance-tool) `JS` - Tool to fetch cluster's balance, using Subgrph under the hood.
- [bApp example](https://github.com/ssvlabs/examples) `GPL | TS` - An Example of how Based Application can be used and built.
- [DKG by Randamu](https://github.com/randa-mu/ssv-dkg) `MIT | Go` - Alternative DKG tool, the project is in active development.

#### Operator services

- [Stereum](https://github.com/stereum-dev/ethereum-node/) `MIT | Vue/JS` - Node Setup GUI to simplify the Node Operator setup.
- [eth-docker](https://github.com/eth-educators/eth-docker) `Apache | Shell` - Node Setup GUI to simplify the Node Operator setup.
- [SSV DApp Node Package](https://github.com/dappnode/DAppNodePackage-ssv-generic) `GPL | Shell` - SSV Node Setup Wizard by DApp Node.
- [SSV Stack](https://github.com/ssvlabs/ssv-stack) `Shell` - Boilerplate for SSV Node setup and it's monitoring.
- [Blockops Telescope](https://github.com/blockopsnetwork/telescope) `Apache | Go` - Observability Tool for blockchain nodes including SSV.

---

## Related Concepts
- [What are the bApps (Based Applications)?](https://docs.ssv.network/based-applications/learn/based-applications/)
- [commit-boost client](https://github.com/Commit-Boost/commit-boost-client)
- [Awesome Preconfirmations](https://github.com/NethermindEth/awesome-preconfirmations?tab=readme-ov-file#related-concepts)

---
## How to contribute

#### Suggest improvements

If you have ideas or improvements — **Open an issue** or bring it up in the SSV Discord [#discussions](https://discord.gg/invite/ssvnetworkofficial) channel.

If you see any typos in the tutorials, have a suggestion for better phrasing, or see a bug in the code — **Open a PR**.

#### How to add your project

Add your project to the appropriate category in this README file and create a Pull Request.

**Example project**

- My project name (https://github.com/myrepos/my-awesome-ssv-repo/) `license used` | `languages used` (e.g. `MIT | JS`) - short one sentence repo description 

- **In the PR's description** — One paragraph description talking what my repo is about, how is it useful to SSV network.

---

## LICENSE

	MIT License
