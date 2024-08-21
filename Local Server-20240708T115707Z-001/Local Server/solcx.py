class compile_source:
    def __init__(self, *args, **kwargs):
        pass  # Placeholder for initialization

    def __getitem__(self, key):
        if key == 'abi':
            return [
                {
                    "inputs": [
                        {"internalType": "float", "name": "_temperature", "type": "float"},
                        {"internalType": "uint256", "name": "_heartbeat", "type": "uint256"}
                    ],
                    "name": "addRecord",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "getRecords",
                    "outputs": [
                        {
                            "internalType": "struct HealthData.HealthRecord[]",
                            "name": "",
                            "type": "struct HealthData.HealthRecord[]"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
        elif key == 'bytecode':
            return "0x4C6B0Ee344F3115116140729649C38Abf41f94655"
