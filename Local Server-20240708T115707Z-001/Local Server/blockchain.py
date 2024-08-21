# blockchain.py
from web3 import Web3 # type: ignore
from solcx import compile_source # type: ignore

# Ethereum network configuration
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/0FBQUFBQm1pcEdGcmprWjBsbTVCYnJfT3Bva1JLNXZwMGd2')) 

# Compile the smart contract
compiled_sol = compile_source(
    """
    pragma solidity ^0.8.0;

    contract HealthData {
        struct HealthRecord {
            uint timestamp;
            float temperature;
            uint heartbeat;
        }

        HealthRecord[] public records;

        function addRecord(float _temperature, uint _heartbeat) public {
            records.push(HealthRecord(block.timestamp, _temperature, _heartbeat));
        }

        function getRecords() public view returns (HealthRecord[] memory) {
            return records;
        }
    }
    """,
    output_values=['abi', 'bytecode'],
)

# Get the contract ABI and bytecode
abi = compiled_sol['abi']
bytecode = compiled_sol['bytecode']

# Deploy the contract
HealthData = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = HealthData.constructor().transact({'from': w3.eth.accounts})  
# w3.eth.wait_for_transaction_receipt(tx_hash)

# # Get the deployed contract address
contract_address = '0x4C6B0Ee344F3115116140729649C38Abf41f94655'
# Create a contract instance
health_data_contract = w3.eth.contract(address=contract_address, abi=abi)

def record_data_on_blockchain(temperature, heartbeat):
    """Records health data on the blockchain."""
    
    tx_hash = health_data_contract.functions.addRecord(temperature, heartbeat).transact({'from': w3.eth.accounts[0]})  # Replace with your Ethereum account
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Data recorded on blockchain: {tx_hash.hex()}")

