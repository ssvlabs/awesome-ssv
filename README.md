# Awesome SSV

This repo:

1. showcases how to [create and run LSD staking pool](/RUN_THIS_REPO.md) leveraging ssv.network,
2. helps you **start building**, by maintaining a curated list of [SSV tools & projects & guides](#ssv-projects-&-resources)

## Start BUIDLing

This repo is meant to give you a head start in building a cool prototype of the next big staking app. Build something interesting on top such as transferable NFT validators, Restaking app, or whatever else, and **open PR**.

to **Create and run LSD staking pool**

open [RUN_THIS_REPO.md](RUN_THIS_REPO.md) for instructions.

### Credits

Huge thanks to

- [@RohitAudit](https://github.com/RohitAudit) who develops & maintains all the **backend** magic on whose [repo-Garuda](https://github.com/RohitAudit/ssv-service) this minimalistic LSD staking pool is based on.

- [@nibthebear](https://github.com/TIM88-DOT) who has developed the **frontend**, js deployment, and revamped the **smart contracts**.

## SSV projects & resources

### Get funding

You can hop into SSV discord channel [#devs-support](https://discord.com/channels/723834989506068561/766640777815523330) and get feedback on your ideas. You may also check [active grants](https://grants.ssv.network/) directly. If you are considering applying for one, write in SSV discord and tag @Matty and @MarkoInEther. They will be happy to help you draft a rock star grant application.

### Connect with teams

The best way is via discord channel [#devs-support](https://discord.com/channels/723834989506068561/766640777815523330), ask there, tag the team directly, and also @MarkoInEther and @Matty. They will help you to get to the right person.

---

- [Tools](#tools)

- [Notification services](#notification-services)

- [Staking pools](#staking-pools)

- [Staking services](#staking-services)

- [Operator services](#operator-services)

- [Guides](#guides)

- [How to add your project](#how-to-add-your-project)

---

### Documentation

You can **read the full documentation** at [docs.ssv.network](https://docs.ssv.network/).

### Tools

- [awesome-ssv backend](RUN_BACKEND.md) `MIT | PY`
  This backend scrip in this repo allows has all the necessary functions to easily manage a staking pool. It can be also used separately, just to generate keys or do key splitting.  
  It has these actions:

      - Create Validator keys (for Deposit)
      - generate-keyshares (for SSV contract)
      - deposit-keyshares
      - deposit-validators

#### Validator key splitting / distribution (key shares creation)

To use the SSV network a validator key needs to be split into keyshares, which then need to be encrypted for chosen operators. You can use these tools for it, and to know more read the [documentation](https://docs.ssv.network/developers/tools/ssv-key-distributor).

- [SSV Keys - validator key splitting tool by Blox](https://github.com/bloxapp/ssv-keys) `MIT | JS`

This is a validator key splitting tool library implemented in JS/TS. It can be used to split validator keys and generate keyshares. It is easily implemented as an npm package. You can also [download executable cli](https://github.com/bloxapp/ssv-keys) of this tool.

- [SSV Keys Go implementation by ChainUp](https://github.com/duktig666/ssv-keys-go) `Apache-2.0 | Go`

This is the Go implementation of the [ssv-keys repository](https://github.com/bloxapp/ssv-keys). The use case is for those who prefer generating keyshares using the Go language over Javascript/Typescript.

- [SSV Key GUI by Starkeys](https://github.com/stakestar/starkeys) `MIT | Electron/React`

StarKeys is a cross-platform SSV Key Distribution application that runs on Mac, Linux, and Windows using the Electron framework. The implementation is designed to operate fully offline. StarKeys offers a convenient and user-friendly way for users to interact with the SSV Distribution.

#### Validator key generation / management

- [SSV-Tool by Nodeplus](https://github.com/nodeplusio/ssv-tool) - command-line utility for registering validators and estimating costs of operation | MIT | JS

To make the registration process easier, the tool manages key generation and smart contract interaction; the user only needs to provide keystore files and operator ids. This tool also provides a flexible method for estimating operation expenses to match various operation assumptions. SSV V2 is currently being tested; SSV V3 and batch processing support will be added shortly.

#### Distributed (validator) key generation

This technology unlocks trustless staking use cases and removes the necessity for a single party to safeguard the full validator key.

- [Rockx DKG](https://github.com/RockX-SG/frost-dkg-demo/) — frost based Distributed key generation (DKG)

This repository provides a collection of services that demonstrate frost based DKG functionality, which generates a validator public key and splits shares among operators. The services included are an API service, a messenger service, a Node service for keygen initiation, results viewing, and deposit data retrieval for Ethereum 2.0 deposit contract

### Notification services

- [HAL](https://app.hal.xyz/) - The Crypto Notification System

Hal has built a custom Notify Recipe for SSV that allows SSV users to automatically monitor and get custom notifications for monitoring, operation runway, operator fee change, and many more SSV protocol-related events. Users will set up their notifications using the Hal Notify app and then receive their notifications on the channel or their preference (email, telegram, discord, etc.)

- [Hellman - allerts](https://alert.hellman.team/metrics) / [Hellman - repo](https://github.com/HellmanResearch)

HellmanAlert is a monitoring of SSV.Network, which mainly provides operators/users with 7\*24 hours monitoring of account balance, operation performance & status.

### Staking pools

- [GARUDA](https://github.com/RohitAudit/ssv-service) - `MIT | PY, SOL` Staking pool, with backend bot handling validator creation, splitting, and registration.

User stakes their ETH to a staking contract through which he is given a liquid staked derivative token called roETH. That's it! Users can just relax and wait for their roETH to compound over time and till then use the same tokens in other DeFi protocols

- [FRENS](github.com/frens-pool) - community staking app, stake represented by NFTs

Staking pools for peer-to-peer staking on trusted node operators (friends)

### Staking services

- [Casimir](https://github.com/consensusnetworks/casimir) - Decentralized self custody staking and asset management for Ethereum and more

Casimir is a cross-chain digital asset management platform that allows users to manage all of their digital assets from NFTs to Staking across chains and wallets in a simple UI that enables users to retain privacy and self-custody.

- [Blockscape Network](https://github.com/BlockscapeNetwork/ssv-institutional-staking) — KYC-compliant Ethereum staking powered by SSV

Don't let compliance and regulatory requirements get in your way. We allow any institution to securely store and stake ETH assets in an insured, audited, and reward-generating way.

### Operator services

- [Stereum](https://github.com/stereum-dev/ethereum-node/) - a Node Setup GUI that built an easy SSV Network Operator setup

If you got an Ubuntu server, you can use Stereum's Node tool to connect to it and install/maintain an SSV Operator without having to access the CLI. If you have any questions about it, let us know 😄.

- [ChainUp Cloud](https://cloud.chainup.com/) — ChainUp Cloud is an all-in-one SSV platform

Our SSV services include operator support and staking options to help you maximize your returns and partake in decentralization. Our team of experienced blockchain team is dedicated to providing the highest level of support, and we utilize industrial-grade infrastructure to ensure the reliability and security of our services. Our goal is to help you maximize your returns and achieve your business objectives.

### Tutorials

Check the **[Tutorials folder](/tutorials)**

- [Video - How To Setup a Node On SSV Testnet V2](https://www.youtube.com/watch?v=X85Sxe9yS5U)

- [Video - run SSV node in 10 minutes🚀](https://www.youtube.com/watch?v=HFb4uxHC50w)

## How to contribute

- **introduce a new features** by creating an issue, if they are usefull for the ecosystem ssv dao may fund you developing them! join discord hang out in #dev-support channel!

- **correct error** by opening a PR.

### How to add your project

Add your project to the appropriate category in this README file and create a pull request.

**Example project**

- [My project name](https://github.com/myrepos/my-awesome-ssv-repo) — short one sentence repo description |`license used` | `languages used` (e.g. `MIT | JS`)

One paragraph description talking what my repo is about, how is it special. Please keep your description concise, the limit is 80 words.

### LICENSE

MIT License
