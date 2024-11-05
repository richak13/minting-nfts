from web3 import Web3
from eth_account.messages import encode_defunct
import random
import json

# Avalanche Fuji Testnet RPC URL
AVAX_RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(AVAX_RPC_URL))

# Contract address and ABI file path
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
with open("NFT.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Private key for signing (replace this with your private key)
private_key = "b821b64959666b171c69a586e911fbcb08af0b7dd373ca5e6f42982a0366184c"
account = w3.eth.account.from_key(private_key)
address = account.address

# Middleware setup (needed for Avalanche's Proof of Authority)
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Mint an NFT by calling the 'claim' function with a random nonce
def mint_nft():
    nonce = random.randint(1, 1000000)  # Generate a random nonce
    tx = contract.functions.claim(nonce).build_transaction({
        'from': address,
        'nonce': w3.eth.get_transaction_count(address),
        'gas': 250000,
        'gasPrice': w3.eth.gas_price
    })

    # Sign and send the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Minting successful, transaction hash: {tx_hash.hex()}")

    # Extract and print the token ID from the receipt logs (ERC721 Transfer event)
    token_id = tx_receipt['logs'][0]['topics'][3]
    print(f"Token ID: {int(token_id.hex(), 16)}")

# Function to sign the challenge
def signChallenge(challenge):
    acct = w3.eth.account.from_key(private_key)
    signed_message = w3.eth.account.sign_message(challenge, private_key=acct._private_key)
    return acct.address, signed_message.signature

# Verification function to test the signature
def verifySig():
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge(challenge)
    return w3.eth.account.recover_message(challenge, signature=sig) == address

# Main execution
if __name__ == '__main__':
    # Mint the NFT first
    mint_nft()
    
    # Then test the sign and verify functionality
    if verifySig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")
