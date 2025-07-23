import os, requests

RPC_URL = os.getenv("RPC_URL")

def fetch_transactions(address, start_block=0, end_block="latest"):
    payload = {
        "jsonrpc":"2.0",
        "method":"eth_getLogs",
        "params":[{
            "fromBlock": hex(start_block),
            "toBlock":   end_block,
            "address":   address.lower()
        }],
        "id":1
    }
    resp = requests.post(RPC_URL, json=payload)
    resp.raise_for_status()
    return resp.json().get("result", [])
