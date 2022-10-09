pragma solidity ^0.8.0;

import "./interfaces/ISSVNetwork.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract KeysManager {

    struct Validator {
        bytes pubkey;
        uint32[] operatorIDs;
    }

    Validator[] public validators;
    uint32[4] OperatorIDs;
    address WhitelistKeyGenerator;
    address SSVTOKEN;
    address SSV_ADDRESS;
    event RegisteredValidator(bytes pubkey);
    constructor(address ssv_contract, address ssv_token,address keyGenerator,uint32[4] memory ids){
        OperatorIDs = ids;
        SSV_ADDRESS = ssv_contract;
        SSVTOKEN = ssv_token;
        WhitelistKeyGenerator = keyGenerator;
    }

    function getOperators() public view returns( uint32[4] memory){
        return OperatorIDs;
    }

    function submitValidatorShares(bytes calldata publicKey,
        uint32[] calldata operatorIds,
        bytes[] calldata sharesPublicKeys,
        bytes[] calldata sharesEncrypted,
        uint256 amount) external {
        require(msg.sender==WhitelistKeyGenerator,"Only whitelisted address can submit the key");
        IERC20(SSVTOKEN).approve(SSV_ADDRESS,amount);
        ISSVNetwork(SSV_ADDRESS).registerValidator(publicKey, operatorIds, sharesPublicKeys, sharesEncrypted, amount);
        validators.push(Validator(publicKey,operatorIds));
    }

}