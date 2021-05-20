import brownie 

def test_balance_owner_decreased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    owner_balance = token.balanceOf(accounts[0], {'from': accounts[5]})

    token.approve(accounts[5], 10**18, {'from': accounts[0]})

    token.transferFrom(accounts[0], accounts[1], 10**18, {'from': accounts[5]})

    assert owner_balance == token.balanceOf(accounts[0]) + 10**18

def test_balance_recipient_increased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    recipient_balance = token.balanceOf(accounts[1], {'from': accounts[5]})

    token.approve(accounts[5], 10**18, {'from': accounts[0]})
    allowance = token.allowance(accounts[0], accounts[5])

    token.transferFrom(accounts[0],accounts[1], 10**18, {'from': accounts[5]})

    assert recipient_balance == token.balanceOf(accounts[1]) - 10**18

def test_allowance_changes_after_approve(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})

    allowance_before_approve = token.allowance(accounts[0], accounts[5])

    token.approve(accounts[5], 10**18, {'from': accounts[0]})

    allowance_after_approve = token.allowance(accounts[0], accounts[5])

    assert allowance_after_approve == 10**18
    assert allowance_before_approve == 0

def test_allowance_changes_after_transfer_from(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})

    token.approve(accounts[5], 10**18, {'from': accounts[0]})

    allowance_before_transfer = token.allowance(accounts[0], accounts[5])

    token.transferFrom(accounts[0],accounts[1], 10**18, {'from': accounts[5]})

    allowance_after_transfer = token.allowance(accounts[0], accounts[5])

    assert allowance_after_transfer == 0
    assert allowance_before_transfer == 10**18

def test_approval_and_transfering_events_fire(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})

    tx = token.approve(accounts[5], 10**18, {'from': accounts[0]})

    tx1 = token.transferFrom(accounts[0],accounts[1], 10**18, {'from': accounts[5]})

    assert len(tx.events) == 1
    assert tx.events["approval"].values() == [accounts[0], accounts[5], 10**18]
    assert len(tx1.events) == 1
    assert tx1.events["transfering"].values() == [accounts[0], accounts[1], 10**18]