import brownie
def test_balance_sender_decreased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    sender_balance = token.balanceOf(accounts[0], {'from': accounts[5]})

    token.transfer(accounts[1], 10**18, {'from': accounts[0]})

    assert sender_balance == token.balanceOf(accounts[0]) + 10**18

def test_balance_recipient_increased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    recipient_balance = token.balanceOf(accounts[1], {'from': accounts[1]})

    token.transfer(accounts[1], 10**18, {'from': accounts[0]})

    assert recipient_balance == token.balanceOf(accounts[1]) - 10**18

def test_total_suply_not_affected(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    total_suply = token.getTotalSuply()
    token.transfer(accounts[1], 10**18, {'from': accounts[0]})

    assert total_suply == token.getTotalSuply()

def test_transfer_to_self(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from': accounts[5]})
    sender_balance = token.balanceOf(accounts[0], {'from': accounts[0]})

    token.transfer(accounts[0], 10**18, {'from': accounts[0]})

    assert sender_balance == token.balanceOf(accounts[0], {'from': accounts[0]})

def test_zero_transfer(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    sender_balance = token.balanceOf(accounts[0], {'from': accounts[0]})
    recipient_balance = token.balanceOf(accounts[1], {'from': accounts[1]})

    token.transfer(accounts[1], 0, {'from': accounts[0]})

    assert sender_balance == token.balanceOf(accounts[0], {'from': accounts[0]})
    assert recipient_balance == token.balanceOf(accounts[1], {'from': accounts[1]})

def test_transfer_event_fires(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token.addOwner({'from' : accounts[1]})
    amount = token.balanceOf(accounts[0], {'from': accounts[0]})
    tx = token.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["transfering"].values() == [accounts[0], accounts[1], amount]
