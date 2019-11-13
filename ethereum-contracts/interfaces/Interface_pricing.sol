pragma solidity ^0.5.11;

/**
 * @dev Interface of the Pricing contract
 */

interface IPricing {
    /// CALLER FUNCTIONS
    /**
     * @dev Returs the discount being used by a provider
     */
    function discount() public view returns(uint256);

    /**
     * @dev Returs the final price exercised by a provider
     */
    function finalPrice() public view returns(uint256);

    /**
     * @dev Returns the address of the provider who ownes the contract.
     */
    function owner() public view returns(payable address);

    /**
     * @dev Returns True if production peak, and False if not production peak.
     */
    function productionPeak() public view returns(bool);

    /// TRANSACTION FUNCTIONS

    /**
     * @dev Creates a Pricing contract
     * @param price - initial price to be set on contract
     * @param caller - address of provider that is attached to this contract
     */
    function constructor(uint256 price, address payable caller) public;

    /**
     * @dev Set price rate to newPrice
     * @param newPrice - price to set
     * This function is only accessible by the owner of the contract
     */
    function adjustPricing(uint256 newPrice) public onlyOwner ;

    /**
     * @dev Set discount rate to newDiscount
     * @param newDiscount - discount to set
     * This function is only accessible by the owner of the contract
     */
    function adjustDiscount(uint256 newDiscount) public onlyOwner ;
}


