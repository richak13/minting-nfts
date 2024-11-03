from web3 import Web3
from eth_account.messages import encode_defunct
import random

def signChallenge( challenge ):

    w3 = Web3()

    sk = "1cde024c70d3deff5b8bec33aba4d14f542be3200f53ffc4853df6fdaa475a8a"

    acct = w3.eth.account.from_key(sk)

    signed_message = acct.sign_message(challenge)

    return acct.address, signed_message.signature



def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    
    # Call signChallenge to sign the challenge
    address, sig = signChallenge(challenge)

    # Recover the address from the signed message and verify
    w3 = Web3()
    return w3.eth.account.recover_message(challenge, signature=sig) == address
    

if __name__ == '__main__':
    """
        Test your function
    """
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

