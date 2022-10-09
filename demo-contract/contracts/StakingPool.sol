pragma solidity ^0.8.0;

import "./interfaces/IDepositContract.sol";
import "./interfaces/ICommon.sol";
import "./interfaces/IRoEth.sol";
import "./Common.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract StakingPool is ReentrancyGuard {
    uint256 roETHMinted = 0;
    address WhitelistKeyGenerator;
    address _admin;
    address public WITHDRAWAL_ADDRESS;
    IDepositContract immutable DepositContract;
    ICommon immutable CommonContract;
    uint256 public immutable VALIDATOR_AMOUNT = 32 * 1e18;

    event UserStaked(address user_address, uint256 amount);
    event PubKeyDeposited(bytes pubkey);

    constructor(address keyGenerator, address depositAddress, address common,address withdrawal){
        WITHDRAWAL_ADDRESS = withdrawal;
        WhitelistKeyGenerator = keyGenerator;
        DepositContract = IDepositContract(depositAddress);
        CommonContract = ICommon(common);
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
        require(msg.sender == WhitelistKeyGenerator, "Only whitelisted address can submit the key");
        DepositContract.deposit{value : VALIDATOR_AMOUNT}(pubkey, withdrawal_credentials, signature, deposit_data_root);
        emit PubKeyDeposited(pubkey);
    }

}