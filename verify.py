from web3 import Web3
from eth_account.messages import encode_defunct
import random
import json

# Connect to Avalanche Fuji Testnet
AVAX_RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(AVAX_RPC_URL))

# Verify connection to network
if w3.is_connected():
    print("Connected to Avalanche Fuji Testnet")
else:
    print("Failed to connect to Avalanche Fuji Testnet")

# Contract details
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
with open("NFT.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Set up account with your private key
private_key = "b821b64959666b171c69a586e911fbcb08af0b7dd373ca5e6f42982a0366184c"
account = w3.eth.account.from_key(private_key)
address = account.address
print(f"Using account: {address}")

# Check AVAX balance
balance = w3.eth.get_balance(address)
print(f"Account balance: {w3.from_wei(balance, 'ether')} AVAX")

# Mint NFT function
def mint_nft():
    nonce_value = random.randint(1, 1000000)  # Generate a random nonce
    nonce_bytes32 = Web3.to_bytes(hexstr=hex(nonce_value))  # Convert nonce to bytes32

    try:
        # Call the claim function with the address and nonce in bytes32 format
        tx = contract.functions.claim(address, nonce_bytes32).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gas': 300000,  # Increased gas limit
            'gasPrice': w3.to_wei('30', 'gwei')
        })

        # Sign and send the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction hash: {tx_hash.hex()}")

        # Wait for receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        print("Minting successful:", tx_receipt)

        # Extract and print the token ID
        token_id = tx_receipt['logs'][0]['topics'][3]
        print(f"Minted NFT with Token ID: {int(token_id.hex(), 16)}")
    except Exception as e:
        print("Minting failed:", e)

# Function to sign the challenge for verification
def signChallenge(challenge):
    acct = w3.eth.account.from_key(private_key)
    signed_message = w3.eth.account.sign_message(challenge, private_key=acct._private_key)
    return acct.address, signed_message.signature

# Verification function to test the signature
def verifySig():
    """
    This is essentially the code that the autograder will use to test signChallenge.
    """
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge(challenge)
    return w3.eth.account.recover_message(challenge, signature=sig) == address

# Main execution
if __name__ == '__main__':
    # Mint the NFT
    print("Starting NFT minting process...")
    mint_nft()

    # Then test the sign and verify functionality
    print("Starting challenge verification...")
    if verifySig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")
