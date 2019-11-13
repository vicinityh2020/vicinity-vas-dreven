pragma solidity ^0.5.11;

/// @title DoubleSigWalletFactory - Factory contract that allows creation of contracts type DoubleSigWallet
/// @author João Quintanilha - <jquintanilha@ubiwhere.com>

import "./DoubleSigWallet.sol";
import "./Pricing.sol";

contract DoubleSigWalletFactory {
    /*
    *Storage
    */
    // mapping(  user =>  mapping( provider => doublesigwallet ))
    mapping(address => mapping ( address => DoubleSigWallet)) public enduserProviderDoubleSigMap;
    mapping(address => DoubleSigWallet[]) public enduserDoubleSigMap;

    /*
    *Events
    */
    event DoubleSigCreated(DoubleSigWallet doubleSigWallet);

    /*
    *Modifiers
    */
    modifier doesntHaveDoubleMultiSig(address _enduser, Pricing _pricingAddress){
        require(address(enduserProviderDoubleSigMap[_enduser][_pricingAddress.owner()]) == address(0),
            "Enduser already has Double Sig Wallet with this provider!");
            _;
    }

    modifier addressIsValid(Pricing _pricingAddress){
        require(address(_pricingAddress) != address(0), "Pricing contract must exist!");
        _;
    }

    /// @dev creates a new doubleSig contract with the msg.sender as owner attached to a
    /// princing contract from a certain provider
    /// @param _pricingAddress - pricing contract to agree on
    function createDoubleSig(Pricing _pricingAddress)
        public doesntHaveDoubleMultiSig(msg.sender, _pricingAddress) addressIsValid(_pricingAddress){

        DoubleSigWallet newDoubleSigWallet = new DoubleSigWallet(msg.sender, address(_pricingAddress));
        enduserProviderDoubleSigMap[msg.sender][_pricingAddress.owner()] = newDoubleSigWallet;
        enduserDoubleSigMap[msg.sender].push(newDoubleSigWallet);

        emit DoubleSigCreated(newDoubleSigWallet);
    }

    function getDoubleSigsByUser(address _enduser) public view returns(DoubleSigWallet[] memory){
        return enduserDoubleSigMap[_enduser];
    }

}
