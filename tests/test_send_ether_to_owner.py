
import brownie

def test_sender_balance_increases(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token.receiveEther({'from' : accounts[5], 'value': 10**18})
    before = accounts[0].balance()
    token.payEtherToOwner({'from' : accounts[0]})
    after = accounts[0].balance()

    assert after - before == 10**18

def test_contract_balance_decreases(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token.receiveEther({'from' : accounts[5], 'value': 10**18})
    before = token.balance()
    token.payEtherToOwner({'from' : accounts[0]})
    after = token.balance()

    assert before - after == 10**18

def test_zero_deposit_after_paying(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token.receiveEther({'from' : accounts[5], 'value': 10**18})
    token.payEtherToOwner({'from' : accounts[0]})
    deposit = token.getOwnerDeposit({'from' : accounts[0]})

    assert deposit == 0

