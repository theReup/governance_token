import brownie
def test_balance_increased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    owner_balance = token.balanceOf(accounts[0], {'from': accounts[5]})

    token._mint(10**18, accounts[0], {'from': accounts[5]})

    assert owner_balance == token.balanceOf(accounts[0], {'from': accounts[5]}) - 10**18

def test_total_suply_increased(accounts, token):
    token.addOwner({'from' : accounts[0]})
    total_suply = token.getTotalSuply()

    token._mint(10**18, accounts[0], {'from' : accounts[5]})

    assert total_suply == token.getTotalSuply() - 10**18

def test_mint_to_self(accounts, token):
    token.addOwner({'from' : accounts[5]})
    owner_balance = token.balanceOf(accounts[5], {'from': accounts[5]})

    token._mint(10**18, accounts[5], {'from': accounts[5]})

    assert owner_balance == token.balanceOf(accounts[5], {'from': accounts[5]}) - 10**18

def test_mint_event_fires(accounts, token):
    token.addOwner({'from' : accounts[0]})
    tx = token._mint(10**18, accounts[0], {'from' : accounts[5]})

    assert len(tx.events) == 1
    assert tx.events["mint"].values() == [10**18, accounts[0]]
