from web3 import Web3
from eth_account.messages import encode_defunct
import random
import json

# Connect to Avalanche Fuji Testnet
AVAX_RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"  # Use the official Avalanche RPC or another endpoint
w3 = Web3(Web3.HTTPProvider(AVAX_RPC_URL))

# Load the ABI from the NFT.abi file
with open("NFT.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Contract details
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # Contract address on Fuji Testnet

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Set up account
private_key = "1cde024c70d3deff5b8bec33aba4d14f542be3200f53ffc4853df6fdaa475a8a"  # Replace with your actual private key (keep it secure!)
account = w3.eth.account.from_key(private_key)
address = account.address

# Middleware setup (required for Proof of Authority networks)
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

    # Sign the transaction with the private key
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Minting successful, transaction hash: {tx_hash.hex()}")

    # Verify ownership
    token_id = tx_receipt['logs'][0]['topics'][3]  # Extract token ID from the logs (ERC721 Transfer event)
    print(f"Token ID: {int(token_id.hex(), 16)}")

mint_nft()

# signChallenge function for challenge verification
def signChallenge(challenge):
    w3 = Web3()  # Initiate Web3 instance
    acct = w3.eth.account.from_key(private_key)
    signed_message = w3.eth.account.sign_message(challenge, private_key=acct._private_key)
    return acct.address, signed_message.signature

# Verification function to test the signature
def verifySig():
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge(challenge)
    return w3.eth.account.recover_message(challenge, signature=sig) == address

# Testing the solution
if __name__ == '__main__':
    if verifySig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")
