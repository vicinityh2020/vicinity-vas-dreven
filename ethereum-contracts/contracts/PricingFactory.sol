pragma solidity ^0.5.11;

/// @title PricingFactory - Factory contract that allows creation of contracts type Pricing
/// @author João Quintanilha - <jquintanilha@ubiwhere.com>

import "./Pricing.sol";

contract PricingFactory {

    /*
     *  Storage
     */
    mapping(address => Pricing) providerPricingMap;
    Pricing[] deployedPricings;

    /*
     *  Events
     */
    event NewPricing(Pricing newPricing);

    /*
     *  Modifiers
     */
    /// @dev Restrictions to create pricing contract
    modifier pricingRestrictions {
        require(address(providerPricingMap[msg.sender]) == address(0), "This provider already owns a pricing contract!");
        _;
    }

    /// @dev creates a new Pricing contract with the msg.sender as owner
    /// @param price uint256 initializes te contract price rate.
    function createPricing(uint256 price) public pricingRestrictions {
        require(price >= 0, "Price must be bigger or equal than 0");
        Pricing newPricing = new Pricing(price, msg.sender);
        deployedPricings.push(newPricing);
        providerPricingMap[msg.sender] = newPricing;
        emit NewPricing(newPricing);
    }

    /// @dev returns all the existing pricing contracts created through this factory
    function getAllDeployedPricings() public view returns (Pricing[] memory) {
        return deployedPricings;
    }

    /// @dev returns the deployed Pricing address to a specific provider
    /// @param provider address provider key to lookup in mapping
    function getDeployedPricingByProvider(address provider) public view returns (Pricing){
        return providerPricingMap[provider];
    }

    /// @dev returns the nr of deployed Pricing contracts through this factory
    function getNrOfDeployedPricings() public view returns (uint256) {
        return deployedPricings.length;
    }
}
