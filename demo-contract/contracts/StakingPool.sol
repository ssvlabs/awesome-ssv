pragma solidity ^0.8.0;

import "./interfaces/IDepositContract.sol";
import "./interfaces/ICommon.sol";
import "./interfaces/IRoEth.sol";
import "./Common.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./interfaces/ISSVNetwork.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StakingPool is ReentrancyGuard {
    uint256 roETHMinted = 0;
    address WhitelistKeyGenerator;
    address public WITHDRAWAL_ADDRESS;
    IDepositContract immutable DepositContract;
    ICommon immutable CommonContract;
    uint256 public immutable VALIDATOR_AMOUNT = 32 * 1e18;
    address SSV_TOKEN;
    address SSV_ADDRESS;
    uint32[4] OperatorIDs;
    bytes[] public Validators;

    event UserStaked(address user_address, uint256 amount);
    event PubKeyDeposited(bytes pubkey);

    constructor(address keyGenerator,
        address depositAddress,
        address common,
        address withdrawal,
        address ssv_contract,
        address ssv_token,
        uint32[4] memory operator_ids){
        WITHDRAWAL_ADDRESS = withdrawal;
        WhitelistKeyGenerator = keyGenerator;
        DepositContract = IDepositContract(depositAddress);
        CommonContract = ICommon(common);
        SSV_ADDRESS = ssv_contract;
        SSV_TOKEN = ssv_token;
        OperatorIDs = operator_ids;
    }

    function stake() public payable {
        require(msg.value > 0, "Can't stake zero amount");
        uint256 amount_minted = msg.value * IRoEth(CommonContract.getRoETH()).sharePrice() / 1e18;
        IRoEth(CommonContract.getRoETH()).mint(msg.sender, amount_minted);
        emit UserStaked(msg.sender, msg.value);
    }

    function depositValidator(bytes calldata pubkey,
        bytes calldata withdrawal_credentials,
        bytes calldata signature,
        bytes32 deposit_data_root) external {
        DepositContract.deposit{value : VALIDATOR_AMOUNT}(pubkey, withdrawal_credentials, signature, deposit_data_root);
        emit PubKeyDeposited(pubkey);
    }

    function depositShares(bytes calldata pubkey,
        uint32[] calldata operatorIds,
        bytes[] calldata sharesPublicKeys,
        bytes[] calldata sharesEncrypted,
        uint256 amount) external {
        require(msg.sender == WhitelistKeyGenerator, "Only whitelisted address can submit the key");
        IERC20(SSV_TOKEN).approve(SSV_ADDRESS, amount);
        ISSVNetwork(SSV_ADDRESS).registerValidator(pubkey, operatorIds, sharesPublicKeys, sharesEncrypted, amount);
        Validators.push(pubkey);
    }

}