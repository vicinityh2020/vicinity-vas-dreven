pragma solidity ^0.5.11;

/// @title DoubleSigWallet - Allows two parties to agree on transactions before execution.
/// @author João Quintanilha - <jquintanilha@ubiwhere.com>

import "./Pricing.sol";

// Import OpenZeppelin's ERC20 interface defenition
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";


contract DoubleSigWallet {
    IERC20 public DAI;

    /*
     *  Events
     */
    event NewTransaction(uint256 transactionId);
    event EndUserSigned(bool signed);

    /*
     *  Storage
     */
    address public enduser;
    address payable public provider;
    Pricing pricingContract;
    bool public enduserSig;
    uint256 lockedPrice;
    mapping (uint => Transaction) public transactions;
    uint256 transactionCount;

    struct Transaction {
        address destination;
        uint value;
        uint256 meterValue;
        uint256 price;
    }

    /*
     *  Modifiers
     */
    modifier validContructorRequirements(address _enduser, address _pricing) {
        require(_pricing != address(0) && _enduser != address(0), "Provider and pricing contract must have addresses");
        _;
    }

    modifier isEnduser(address _addr) {
        require(_addr == enduser, "Only owner enduser can access this function this contract!");
        _;
    }

    modifier isProvider(address _addr){
        require(_addr == provider, "Only the provider can charge the enduser!");
        _;
    }

    modifier isSignedByEnduser(){
        require(enduserSig == true, "Enduser must have agreed on price rate");
        _;
    }

     /*
     * Public functions
     */
    /// @dev Contract constructor sets initial owner and provider number of confirmations
    /// @param _pricing - address of the pricing contract this contract references
    /// @param _enduser - address of the end user who owns this contract
    constructor(address _enduser, address _pricing) public validContructorRequirements(_enduser, _pricing) {

        DAI = IERC20(0xC4375B7De8af5a38a93548eb8453a498222C4fF2);
        pricingContract = Pricing(_pricing);
        provider = pricingContract.owner();
        require(provider != _enduser, "Provider can not be enduser!");
        enduser = _enduser;
        transactionCount = 0;
        enduserSig = false;
    }


    /// @dev Function that returns current available balance on this contract
    function balanceOfContract() public view returns(uint256){
        return DAI.balanceOf(address(this));
    }

    /// @dev Function that Enduser uses to sign the contract and lock the price rate
    function sign() public isEnduser(msg.sender){
            enduserSig = true;
            lockedPrice = getPrice();
            emit EndUserSigned(enduserSig);
    }

    /// @dev Function that Enduser uses to delete their signature from the contract
    function unsign() public isEnduser(msg.sender){
            enduserSig = false;
    }

    /// @dev Function accessed only by Provider to charge the enduser according to a metervalue
    /// @param _meterValue - kW/h consumed
    function chargeEndUser(uint256 _meterValue) public isProvider(msg.sender) isSignedByEnduser {
        require(balanceOfContract() >= (_meterValue * lockedPrice), "Contract does not have enough funds to charge");

        DAI.transfer(msg.sender, (_meterValue * lockedPrice));

        transactions[transactionCount] = Transaction({
            destination: msg.sender,
            value: _meterValue * getPrice(),
            meterValue:_meterValue,
            price: getPrice()
        });

        emit NewTransaction(transactionCount);
        transactionCount += 1;
        enduserSig = false;
    }

    /// @dev Function accessed only by Provider to charge the entire balance of enduser
    /// meaning metervlaue excided the available
    function zerateEndUser() public isProvider(msg.sender) isSignedByEnduser {
        uint v = balanceOfContract();
        DAI.transfer(msg.sender, balanceOfContract());

        transactions[transactionCount] = Transaction({
            destination: msg.sender,
            value: v,
            meterValue: 0,
            price: getPrice()
        });

        emit NewTransaction(transactionCount);
        transactionCount += 1;
        enduserSig = false;
    }

    /*
     * Internal functions
     */

    /// @dev Function retrieves the price practiced by the pricing contract of one provider
    function getPrice() public view  returns(uint256) {

       return  pricingContract.finalPrice();
    }
}
