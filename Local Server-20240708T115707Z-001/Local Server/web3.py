class Web3:
    def __init__(self, *args, **kwargs):
        pass  

    class HTTPProvider:
        def __init__(self, *args, **kwargs):
            pass  

    class eth:
        class contract:
            def __init__(self, *args, **kwargs):
                pass  # 

            def constructor(self):
                return self

            def transact(self, *args, **kwargs):
                print("Transaction sent (0x4C6B0Ee344F3115116140729649C38Abf41f94655")
                return "0x1234567890abcdef"  #  transaction hash

        def wait_for_transaction_receipt(self, tx_hash):
            print(f"Transaction receipt received (durmmy): {tx_hash}")
            return {"status": 1}  #  transaction receipt

        class accounts:
            def __getitem__(self, index):
                return "0x4C6B0Ee344F3115116140729649C38Abf41f94655"  #  account address

