pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IDepositContract.sol";
import "./interfaces/mocks/ISSVNetwork.sol";
import "./SSVETH.sol";

contract StakingPool is ReentrancyGuard, Ownable {
    address public WhitelistKeyGenerator;
    address public WITHDRAWAL_ADDRESS;
    IDepositContract immutable DepositContract;
    SSVETH public ssvETH;
    uint256 public immutable VALIDATOR_AMOUNT = 32 * 1e18;
    address public SSV_TOKEN_ADDR;
    address public SSV_CONTRACT_ADDR;
    uint32[4] OperatorIDs;
    bytes[] public Validators;

    address public ssvETH_address;
    address public Oracle_address;

    event UserStaked(address user_address, uint256 amount);
    event PubKeyDeposited(bytes pubkey);
    event OperatorIDsChanged(uint32[4] newOperators);
    event SharePriceUpdated(uint256 newPrice);
    event KeySharesDeposited(
        bytes pubkey,
        uint32[] operatorIds,
        bytes[] sharesPublicKeys,
        bytes[] sharesEncrypted,
        uint256 amount
    );

    constructor(
        address keyGenerator,
        address depositAddress,
        address withdrawal,
        address ssv_contract,
        address ssv_token,
        uint32[4] memory ids
    ) {
        WITHDRAWAL_ADDRESS = withdrawal;
        WhitelistKeyGenerator = keyGenerator;
        DepositContract = IDepositContract(depositAddress);
        SSVETH _ssvETH = new SSVETH();
        ssvETH = SSVETH(address(_ssvETH));
        SSV_CONTRACT_ADDR = ssv_contract;
        SSV_TOKEN_ADDR = ssv_token;
        OperatorIDs = ids;
    }

    // getting operator ids, check operators here https://explorer.ssv.network/
    function getOperators() public view returns (uint32[4] memory) {
        return OperatorIDs;
    }

    /**
     * @notice Set operators
     * @param _newOperators: Array of the the new operators Ids
     */
    function setOperators(uint32[4] memory _newOperators) public onlyOwner {
        OperatorIDs = _newOperators;
        emit OperatorIDsChanged(_newOperators);
    }

    /**
     * @notice Update share price of the staking pool
     * @param _newPrice: New share price amount
     */
    function updateSharePrice(uint256 _newPrice) public onlyOwner {
        ssvETH.changeSharePrice(_newPrice);
        emit SharePriceUpdated(_newPrice);
    }

    /**
     * @notice Stake tokens
     */
    function stake() public payable {
        require(msg.value > 0, "Can't stake zero amount");
        uint256 amount_minted = (msg.value * ssvETH.sharePrice()) / 1e18;
        ssvETH.mint(msg.sender, amount_minted);
        emit UserStaked(msg.sender, msg.value);
    }

    /**
     * @notice Unstake tokens
     * @param _amount: Amount to be unstaked
     */
    function unStake(uint256 _amount) public {
        ssvETH.transferFrom(msg.sender, address(this), _amount);
        uint256 _amount_to_transfer = (_amount / ssvETH.sharePrice()) * 1e18;
        payable(msg.sender).transfer(_amount_to_transfer);
    }

    /**
     * @notice Deposit a validator to the deposit contract
     * @param pubkey: Public key of the validator
     * @param withdrawal_credentials: Withdrawal credentials of the validator
     * @param signature: Signature of the deposit data
     * @param deposit_data_root: Root of the deposit data
     */
    function depositValidator(
        bytes calldata pubkey,
        bytes calldata withdrawal_credentials,
        bytes calldata signature,
        bytes32 deposit_data_root
    ) external {
        // Deposit the validator to the deposit contract
        DepositContract.deposit{value: VALIDATOR_AMOUNT}(
            pubkey,
            withdrawal_credentials,
            signature,
            deposit_data_root
        );
        // Emit an event to log the deposit of the public key
        emit PubKeyDeposited(pubkey);
    }

    /**
     * @notice Deposit shares for a validator
     * @param _pubkey: Public key of the validator
     * @param _operatorIds: IDs of the validator's operators
     * @param _sharesPublicKeys: Public keys of the shares
     * @param _sharesEncrypted: Encrypted shares
     * @param _amount: Amount of tokens to be deposited
     * @dev Callable by the whitelisted address
     */
    function depositShares(
        bytes calldata _pubkey,
        uint32[] calldata _operatorIds,
        bytes[] calldata _sharesPublicKeys,
        bytes[] calldata _sharesEncrypted,
        uint256 _amount
    ) external {
        // Check if the message sender is the whitelisted address
        require(
            msg.sender == WhitelistKeyGenerator,
            "Only whitelisted address can submit the key"
        );
        // Approve the transfer of tokens to the SSV contract
        IERC20(SSV_TOKEN_ADDR).approve(SSV_CONTRACT_ADDR, _amount);
        // Register the validator and deposit the shares
        ISSVNetwork(SSV_CONTRACT_ADDR).registerValidator(
            _pubkey,
            _operatorIds,
            _sharesPublicKeys,
            _sharesEncrypted,
            _amount
        );
        // Add the public key to the list of validators
        Validators.push(_pubkey);
        // Emit an event to log the deposit of shares
        emit KeySharesDeposited(
            _pubkey,
            _operatorIds,
            _sharesPublicKeys,
            _sharesEncrypted,
            _amount
        );
    }
}
