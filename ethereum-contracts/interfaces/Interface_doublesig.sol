pragma solidity ^0.5.11;

/**
 * @dev Interface of the DoubleSigWallet contracts
 */

interface IDoubleSigWallet {
    /// CALLER FUNCTIONS
    /**
     * @dev Returs the address of the enduser
     */
    function enduser() public view returns(address);

    /**
     * @dev Returs address of the provider
     */
    function provider() public view returns(payable address);

    /**
     * @dev Returns true is client signed the contract and false if not
     */
    function enduserSig() public view returns(bool);

    /**
     * @dev Returns transaction of position i in mapping
     * @param
     */
    function transactions(uint256 i) public view returns(Transaction);

    /**
     * @dev Returns balance this contract ows in DAI
     */
    function balanceOfContract() public view returns(uint256);

    /**
     * @dev Returns price practiced by the provider attached to this multi sig
     */
    function getPrice() public view returns(uint256);

    /// TRANSACTION FUNCTIONS
    /**
     * @dev Creates a Multisig wallet
     * @param enduser - user that will own the multi sig wallet
     * @param pricing - address of pricing to match with the multi sig wallet
     */
    function constructor(address enduser, address pricing) public;

    /**
     * @dev Sign multisig wallet allowing provider to charge
     * This function is only accessible by the owner of the contract
     */
    function sign() public onlyOwner ;

    /**
     * @dev Unsign multisig wallet not allowing provider to charge
     * This function is only accessible by the owner of the contract
     */
    function unsign() public onlyOwner ;

    /**
     * @dev Charge enduser
     * @param meterValue - current value of meter to be charged upon
     * This function is only accessible by the provider which whom this
     * multi sig wallet was created with
     */
    function chargeEndUser(uint256 meterValue) public onlyOwner ;

    /**
     * @dev Charge client completely
     * This function is only accessible by the provider which whom this
     * multi sig wallet was created with
     */
    function zerateEndUser() public onlyOwner ;
}
}