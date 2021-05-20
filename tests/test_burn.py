import brownie
def test_balance_decreased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    owner_balance = token.balanceOf(accounts[0])
    token._burn(10**18, accounts[0], {'from' : accounts[5]})

    assert owner_balance == token.balanceOf(accounts[0]) + 10**18

def test_total_suply_decreased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    total_suply = token.getTotalSuply()
    token._burn(10**18, accounts[0], {'from' : accounts[5]})

    assert total_suply == token.getTotalSuply() + 10**18

def test_burn_to_self(accounts, token):
    token.addOwner({'from' : accounts[5]})
    token._mint(10**18, accounts[5], {'from' : accounts[5]})
    owner_balance = token.balanceOf(accounts[5])
    token._burn(10**18, accounts[5], {'from' : accounts[5]})

    assert owner_balance == token.balanceOf(accounts[5]) + 10**18

def test_burn_event_fires(accounts, token):
    token.addOwner({'from' : accounts[0]})
    token._mint(10**18, accounts[0], {'from' : accounts[5]})
    tx = token._burn(10**18, accounts[0], {'from' : accounts[5]})

    assert len(tx.events) == 1
    assert tx.events["burn"].values() == [10**18, accounts[0]]


    