from web3 import Web3
from eth_account.messages import encode_defunct
import random

def signChallenge( challenge ):

    w3 = Web3()

    #This is the only line you need to modify
    sk = "b821b64959666b171c69a586e911fbcb08af0b7dd373ca5e6f42982a0366184c"

    acct = w3.eth.account.from_key(sk)

    signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

    return acct.address, signed_message.signature


def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """

    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address

if __name__ == '__main__':
    """
        Test your function
    """
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )
