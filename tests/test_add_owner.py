import brownie
def test_length_increased_by_one(accounts, token):
    old_length = token.getOwnersLength({'from': accounts[0]})
    token.addOwner({'from': accounts[0]})
    new_length = token.getOwnersLength({'from': accounts[0]})

    assert new_length - old_length == 1

def test_add_owner_event_fires(accounts, token):
    tx =  token.addOwner({'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["ownerAddition"].values() == [accounts[0]]