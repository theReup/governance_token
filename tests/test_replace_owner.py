import brownie

def test_const_length(accounts, token):
    token.addOwner({'from': accounts[0]})
    old_length = token.getOwnersLength()
    token.replaceOwner(accounts[0], accounts[1], {'from': accounts[0]})
    new_length = token.getOwnersLength()

    assert old_length - new_length == 0

def test_remove_owner_event_fires(accounts, token):
    token.addOwner({'from': accounts[0]})
    tx =  token.replaceOwner(accounts[0], accounts[1], {'from': accounts[0]})

    assert len(tx.events) == 2
    assert tx.events["ownerRemoval"].values() == [accounts[0]]
    assert tx.events["ownerAddition"].values() == [accounts[1]]
