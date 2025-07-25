// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Multisig {
    uint constant public MAX_OWNER_COUNT = 50; // 设定拥有者最大数量

    mapping(address => bool) public isOwner; // 保存每个地址是否是拥有者
    address[] public owners; // 拥有者地址的数组
    uint public required; // 所需签名的数量

    struct Transaction {
        bool executed; // 交易是否已经执行
        address destination; // 交易目标地址
        uint value; // 交易价值
        bytes data; // 交易数据
    }
    Transaction[] public transactions; // 交易数组

    mapping (uint => mapping (address => bool)) public confirmations; // 保存每个交易的确认情况

    event Confirmation(address indexed sender, uint indexed transactionId); // 确认事件
    event Execution(uint indexed transactionId); // 执行事件
    event ExecutionFailure(uint indexed transactionId); // 执行失败事件

    modifier onlyOwner {
        require(isOwner[msg.sender]);
        _;
    }

    modifier transactionExists(uint transactionId) {
        require(transactions.length > transactionId);
        _;
    }

    modifier confirmed(uint transactionId, address owner) {
        require(confirmations[transactionId][owner]);
        _;
    }

    modifier notConfirmed(uint transactionId, address owner) {
        require(!confirmations[transactionId][owner]);
        _;
    }

    constructor(address[] memory _owners, uint _required) {
        require(_owners.length <= MAX_OWNER_COUNT
            && _required <= _owners.length
            && _required != 0
            && _owners.length != 0);
        for (uint i = 0; i < _owners.length; i++) {
            isOwner[_owners[i]] = true;
        }
        owners = _owners;
        required = _required;
    }

    function confirmTransaction(uint transactionId)
        public
        onlyOwner
        transactionExists(transactionId)
        notConfirmed(transactionId, msg.sender)
    {
        confirmations[transactionId][msg.sender] = true;
        emit Confirmation(msg.sender, transactionId);
        executeTransaction(transactionId);
    }

    function executeTransaction(uint transactionId)
        public
        onlyOwner
        transactionExists(transactionId)
        confirmed(transactionId, msg.sender)
    {
        Transaction storage txn = transactions[transactionId];
        if (!txn.executed) {
            if (isConfirmed(transactionId)) {
                txn.executed = true;
                (bool success,) = txn.destination.call{value: txn.value}(txn.data);
                if (success)
                    emit Execution(transactionId);
                else {
                    emit ExecutionFailure(transactionId);
                    txn.executed = false;
                }
            }
        }
    }

    function isConfirmed(uint transactionId)
        public
        view
        returns (bool)
    {
        uint count = 0;
        for (uint i = 0; i < owners.length; i++) {
            if (confirmations[transactionId][owners[i]])
                count += 1;
            if (count == required)
                return true;
        }
    }
}
