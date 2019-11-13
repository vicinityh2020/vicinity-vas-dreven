pragma solidity ^0.5.11;

/// @title Pricing - Allows creation of contracts to set energy billing properties
/// @author João Quintanilha - <jquintanilha@ubiwhere.com>

contract Pricing {

    address payable public owner; //MSP VAS
    uint256 public finalPrice;
    uint256 normalPrice;
    bool public productionPeak;
    uint256 public discount;

    event PriceChange(uint256 finalPrice);
    event DiscountChange(uint256 discount);

    // Only owner can access endpoints with this tag
    modifier onlyOwner {
        require(msg.sender == owner, "This is not the owner!");
        _;
    }

    /// @dev Initializing pricing contract retains price set and no discounts
    /// @param price  Price rate to be set.
    constructor(uint256 price, address payable caller) public {
        finalPrice = price;
        normalPrice = finalPrice;
        discount = 0;
        owner = caller;
        productionPeak = false;
    }


    /// @dev Change the price rate through this endpoint
    /// @param newPrice uint256 with price rate.
    function adjustPricing(uint256 newPrice) public onlyOwner {
        finalPrice = newPrice;
        normalPrice = finalPrice;
        emit PriceChange(finalPrice);

        updatePricing();
    }



    /// @dev Change the discount rate through this endpoint
    /// @param newDiscount uint256 with discount rate, must be between 0 and 100.
    function adjustDiscount(uint newDiscount) public onlyOwner {
        require(newDiscount >= 0 && newDiscount <= 100, "Discount must be between 0% and 100%!");
        if(newDiscount == 0)
            productionPeak = false;
        else
            productionPeak = true;

        discount = newDiscount;
        updatePricing();

        emit DiscountChange(discount);
    }


    /*
     * Internal functions
     */
    /// @dev Update the current pricing state
    function updatePricing() internal {

        if(productionPeak == true){
            finalPrice = normalPrice * (100-discount)/100;
        }else{
            finalPrice = normalPrice;
        }

    }
}
