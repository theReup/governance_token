pragma solidity ^0.5.0;


import "./SafeMath.sol";

contract governanceToken {

    using SafeMath for uint256;

    event ownerAddition(address indexed owner);
    event ownerRemoval(address indexed owner);
    event mint(uint indexed amount, address indexed owner);
    event burn(uint indexed amount, address indexed owner);
    event transfering(address indexed sender, address indexed recipient, uint amount);
    event etherReceiving(uint indexed amount);
    event payingEtherToOwner(address payable owner, uint indexed amount);
    event approval(address from, address to, uint amount);

    //constants

    uint private totalSuply;
    //storage

    mapping ( address => bool ) isOwner;
    mapping ( address => uint ) private ownersDeposit;//ether amount could be payed to owner 
    mapping ( address => uint ) private _balances;
    mapping ( address => mapping(address => uint)) public allowed;// amount of token you approve to spend by another account
    address payable[] public owners;
    address payable adminAddress;//only address who can mint and burn tokens

    ///@dev Sets address who can mint and burn tokens of each owner
    constructor()
    public
    {
        adminAddress = msg.sender;
    }


    //modifiers

    modifier ownerExists(address owner){
        require(isOwner[owner]);
        _;
    }
    
    modifier ownerDoesNotExists(address owner){
        require(!isOwner[owner]);
        _;
    }

    modifier addressNotNull(address _address){
        require(_address != address(0));
        _;
    }


    /// @dev Fallback function calls reciveEther
    /// Requires that all ether could be deposited
    function()
        external 
        payable
    {
        receiveEther();
    }

    //functions


    /// @dev Allows to add new owner. You can add only yourself 
    function addOwner()
        public
        ownerDoesNotExists(msg.sender)
        addressNotNull(msg.sender)
    {
        
        isOwner[msg.sender] = true;
        owners.push(msg.sender);
        emit ownerAddition(msg.sender);
    }

    /// @dev Allows to remove owner. You can remove only yourself
    /// function finds owner, swaps with last owner and decreases length
    function removeOwner()
        public
        ownerExists(msg.sender)
    {
        isOwner[msg.sender] = false;
        for(uint8 i = 0; i < owners.length - 1; i++){
            if(owners[i] == msg.sender){
                owners[i] = owners[owners.length - 1];
                break;
            }
        }
        owners.length -= 1;
        emit ownerRemoval(msg.sender);
    }

    /// @dev Allows to replace owner with enother not existing
    /// function finds owner, swaps with last owner and replaces with new owner
    /// @param owner is owner to be removed
    /// @param newOwner onwer to be added
    function replaceOwner(address payable owner, address payable newOwner)
        public
        ownerExists(owner)
        ownerDoesNotExists(newOwner)
        addressNotNull(newOwner)
    {
        require(owner == msg.sender);
        for(uint8 i = 0; i < owners.length -1 ; i++){
            if(owners[i] == owner){
                owners[i] = newOwner;
                break;
            }
        }
        isOwner[owner] = false;
        isOwner[newOwner] = true;
        emit ownerAddition(newOwner);
        emit ownerRemoval(owner);
    }

    /// @dev Allows to get quantity of owners outside of contract
    function getOwnersLength()
        external
        view
    returns (uint) 
    {
        return owners.length;
    }

    /// @dev Allows to get owners ether deposit outside of contract
    function getOwnerDeposit()
        external  
        view
        returns (uint)
    {
        return ownersDeposit[msg.sender];
    }

    /// @dev Allows to get contract address outside of contract
    /// Used for test with sending ether to contract
    function contractAddress()
        external 
        view 
        returns(address)
    {
        return address(this);
    }

    /// @dev Allows to get total suply of tokens outside of contract
    function getTotalSuply()
        external 
        view 
        returns (uint)
    {
        return totalSuply;
    }

    /// @dev Allows to get amount of owners tokens
    /// @param account is owner which token balance you want to get
    function balanceOf(address account)
        public
        view
        returns (uint)
    {
        return _balances[account];
    }

    /// @dev Allows to get amount of token approved to spend
    /// @param owner is account who allowes to spend his tokens
    /// @param spender is account who allowed to spend tokens of owner
    function allowance(address owner, address spender) 
        public
        view
        returns (uint)
    {
        return allowed[owner][spender];
    }

    /// @dev Allows to mint tokens only by admin address
    /// @param amount is quantity of tokens to be minted
    /// @param owner is who gets amount of tokens
    function _mint(uint amount, address owner)
        external
    {
        require(isOwner[owner]);
        require(msg.sender == adminAddress);
        totalSuply = totalSuply.add(amount);
        _balances[owner] = _balances[owner].add(amount);
        emit mint(amount, owner);
    }

    /// @dev Allows to burn tokens only by admin address
    /// @param amount is quantity of tokens to be burned
    /// @param owner is whoes tokens will be burned
    function _burn(uint amount, address owner)
        external
    {
        require(isOwner[owner]);
        require(msg.sender == adminAddress);
        require(_balances[owner] >= amount);
        totalSuply = totalSuply.sub(amount);
        _balances[owner] = _balances[owner].sub(amount);
        emit burn(amount, owner);
    }

    /// @dev Allows to transfer tokens from owner to another
    /// @param sender is woner who sends tokens
    /// @param recipient is owner who gets tokens from sender
    /// @param amount is quantity of token to be transfered
    function _transfer(address sender, address recipient, uint amount)
        internal
        addressNotNull(sender)
        addressNotNull(recipient)
    {

        require(_balances[sender] >= amount);
        _balances[sender] = _balances[sender].sub(amount);
        _balances[recipient] = _balances[recipient].add(amount);
        emit transfering(sender, recipient, amount);
    }

    /// @dev Allows to call transfer function from outside of contract
    /// @param to is owner who gets tokens from sender
    /// @param amount is quantity of token to be transfered
    /// requires that you can transfer tokens only from your address
    function transfer(address to, uint amount)
        external
        returns (bool)
    {
        require(isOwner[msg.sender]);
        require(isOwner[to]);
        _transfer(msg.sender, to, amount);
        return true;
    }

    /// @dev Allows receive ether from outside of conctract
    /// After receiving decreases deposits of owners proportional to their token balances
    function receiveEther() 
        public
        payable
    {
        require(totalSuply != 0, "No owners to get ether");
        for(uint i = 0; i < owners.length; i++){
            ownersDeposit[owners[i]] = ownersDeposit[owners[i]].add(
                SafeMath.mul(balanceOf(owners[i]), msg.value) / totalSuply
            );
        }
        emit etherReceiving(msg.value);
    }

    /// @dev Allows owner to get his all ether deposit
    /// After paying sets deposit to zero
    function payEtherToOwner()
        external
    {
        require(isOwner[msg.sender]);
        require(ownersDeposit[msg.sender] != 0);
        msg.sender.transfer(ownersDeposit[msg.sender]);
        emit payingEtherToOwner(msg.sender, ownersDeposit[msg.sender]);
        ownersDeposit[msg.sender] = 0;
    }

    /// @dev Allows approve spending your tokens by another account
    /// @param spender is owner who can spend your tokens
    /// @param amount is quantity of tokens could be spend
    /// Only owner of tokens can set spender of his tokens and amount
    function approve(address payable spender, uint amount)
        external
        returns (bool)
        {
            allowed[msg.sender][spender] = amount;
            emit approval(msg.sender, spender, amount);
            return true;
        }

    /// @dev Allows transfer tokens from sender to recipient by another account 
    /// @param from is address who approved spending his tokens by msg.sender
    /// @param to is recipient who gets tokens from owner
    /// @param amount is quantity of tokens to be transfered to recipient
    /// This transfer can be succesful only after approval amount and address who can spend tokens 
    function transferFrom(address payable from, address payable to, uint amount)
        external
        returns (bool)
    {
        require(isOwner[from]);
        require(isOwner[to]);
        require(allowed[from][msg.sender] >= amount);
        allowed[from][msg.sender] = allowed[from][msg.sender].sub(amount);
        _transfer(from, to, amount);
        return true;
    }
}
