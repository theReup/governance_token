import brownie

def test_length_decreased_by_one(accounts, token):
    token.addOwner({'from': accounts[0]})
    old_length = token.getOwnersLength()
    token.removeOwner( {'from': accounts[0]})
    new_length = token.getOwnersLength()

    assert old_length - new_length == 1

def test_remove_owner_event_fires(accounts, token):
    token.addOwner({'from': accounts[0]})
    tx =  token.removeOwner({'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["ownerRemoval"].values() == [accounts[0]]