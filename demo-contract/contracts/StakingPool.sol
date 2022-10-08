
contract StakingPool {
    struct User {
        uint256 stakedAmount;
        uint256 rewardAmount;
    }
    address WhitelistKeyGenerator;

    mapping (address =>User) user;
    constructor(){

    }

    function stake(){

    }
    function depositEth(bytes calldata pubkey,bytes withdrawal_credentials,bytes calldata signature,bytes calldata deposit_root){

    }
}