import brownie

def test_sender_balance_decreases(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    before = accounts[0].balance()
    token.receiveEther({'from' : accounts[0], 'value': 10**18})
    after = accounts[0].balance()

    assert before - after == 10**18

def test_contract_balance_increases(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    before = token.balance()
    token.receiveEther({'from' : accounts[0], 'value': 10**18})
    after = token.balance()

    assert after - before == 10**18

def test_owners_deposit_increases(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token.addOwner({'from' : accounts[2]})
    token.addOwner({'from' : accounts[3]})

    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token._mint(10**18, accounts[1], {'from' : accounts[5]})
    token._mint(10**18, accounts[2], {'from' : accounts[5]})
    token._mint(10**18, accounts[3], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[0], 'value': 10**18})

    deposit_0 = token.getOwnerDeposit({'from' : accounts[0]})
    deposit_1 = token.getOwnerDeposit({'from' : accounts[1]})
    deposit_2 = token.getOwnerDeposit({'from' : accounts[2]})
    deposit_3 = token.getOwnerDeposit({'from' : accounts[3]})

    assert deposit_0 == 10**18 / 4
    assert deposit_1 == 10**18 / 4
    assert deposit_2 == 10**18 / 4
    assert deposit_3 == 10**18 / 4

def test_deposit_after_mint(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token.addOwner({'from' : accounts[2]})

    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token._mint(10**18, accounts[1], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[5], 'value': 10**18})

    token._mint(2 * 10**18, accounts[2], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[5], 'value': 10**18})

    deposit_0 = token.getOwnerDeposit({'from' : accounts[0]})
    deposit_1 = token.getOwnerDeposit({'from' : accounts[1]})
    deposit_2 = token.getOwnerDeposit({'from' : accounts[2]})

    assert deposit_0 + deposit_1 + deposit_2 == 2 * 10**18
    assert deposit_0 == 10**18 / 2 + 10**18 / 4
    assert deposit_1 == 10**18 / 2 + 10**18 / 4
    assert deposit_2 == 10**18 / 2

def test_deposit_after_burn(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token.addOwner({'from' : accounts[2]})

    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    token._mint(10**18, accounts[1], {'from' : accounts[5]})
    token._mint(2 * 10**18, accounts[2], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[5], 'value': 10**18})

    token._burn(2 * 10**18, accounts[2], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[5], 'value': 10**18})

    deposit_0 = token.getOwnerDeposit({'from' : accounts[0]})
    deposit_1 = token.getOwnerDeposit({'from' : accounts[1]})
    deposit_2 = token.getOwnerDeposit({'from' : accounts[2]})

    assert deposit_0 + deposit_1 + deposit_2 == 2 * 10**18
    assert deposit_0 == 10**18 / 2 + 10**18 / 4
    assert deposit_1 == 10**18 / 2 + 10**18 / 4
    assert deposit_2 == 10**18 / 2

def test_zero_tokens_deposit(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})

    token._mint(10**18, accounts[0], {'from' : accounts[5]})

    token.receiveEther({'from' : accounts[5], 'value': 10**18})

    zero_tokens_deposit = token.getOwnerDeposit({'from' : accounts[1]})

    assert zero_tokens_deposit == 0

def test_ether_receive_event_fires(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    tx = token.receiveEther({'from' : accounts[5], 'value': 10**18})

    assert len(tx.events) == 1
    assert tx.events["etherReceiving"].values() == [10**18]

def test_fallback_calls_receive_ether_function(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    tx = accounts[5].transfer(token.contractAddress(),10**18)

    assert len(tx.events) == 1
    assert tx.events["etherReceiving"].values() == [10**18]