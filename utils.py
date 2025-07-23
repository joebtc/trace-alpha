import os, requests
import streamlit as st

RPC_URL = os.getenv("RPC_URL")

def fetch_transactions(address, start_block=0, end_block="latest"):
    st.markdown("🔍 Debug Info")
    st.write(f"RPC_URL → {RPC_URL}")
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
    st.write(f"Status code → {resp.status_code}")
    st.write(f"Response snippet →\n`json\n{resp.text[:300]}\n```")
    resp.raise_for_status()
    return resp.json().get("result", [])
