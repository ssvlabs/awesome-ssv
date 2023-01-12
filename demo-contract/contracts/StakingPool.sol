pragma solidity ^0.8.0;

import "../interfaces/IDepositContract.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "../interfaces/mocks/ISSVNetwork.sol";
import "./SSVETH.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StakingPool is ReentrancyGuard {
    // uint256 public ssvETHMinted = 0;
    address public WhitelistKeyGenerator;

    address public WITHDRAWAL_ADDRESS;
    IDepositContract immutable DepositContract;
    SSVETH public ssvETH;
    // ICommon immutable CommonContract;
    uint256 public immutable VALIDATOR_AMOUNT = 32 * 1e18;
    address public SSV_TOKEN_ADDR;
    address public SSV_CONTRACT_ADDR; // SSV_ADDRESS
    uint32[4] OperatorIDs;
    bytes[] public Validators;

    address public ssvETH_address;
    address public Oracle_address;

    event UserStaked(address user_address, uint256 amount);
    event PubKeyDeposited(bytes pubkey);

    constructor(address keyGenerator,
        address depositAddress,
        address withdrawal,
        address ssv_contract,
        address ssv_token,
        uint32[4] memory ids){
        WITHDRAWAL_ADDRESS = withdrawal;
        WhitelistKeyGenerator = keyGenerator;
        DepositContract = IDepositContract(depositAddress);
        SSVETH _ssvETH = new SSVETH();
        ssvETH = SSVETH(address(_ssvETH));
        SSV_CONTRACT_ADDR = ssv_contract;
        SSV_TOKEN_ADDR = ssv_token;
        OperatorIDs = ids;
    }

    function getOperators() public view returns( uint32[4] memory){
        return OperatorIDs;
    }

    function stake() public payable {
        require(msg.value > 0, "Can't stake zero amount");
        uint256 amount_minted = msg.value * ssvETH.sharePrice() / 1e18;
        ssvETH.mint(msg.sender, amount_minted);
        emit UserStaked(msg.sender, msg.value);
    }

    function unStake(uint256 amount) public {
        ssvETH.transferFrom(msg.sender, address(this), amount); 
        uint256 amount_to_transfer = amount / ssvETH.sharePrice() * 1e18;
        payable(msg.sender).transfer(amount_to_transfer);
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
        IERC20(SSV_TOKEN_ADDR).approve(SSV_CONTRACT_ADDR, amount);
        ISSVNetwork(SSV_CONTRACT_ADDR).registerValidator(pubkey, operatorIds, sharesPublicKeys, sharesEncrypted, amount);
        Validators.push(pubkey);
    }

}

