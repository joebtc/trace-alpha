import os
import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt
from telegram import Bot

# ─── Helper functions (moved from utils.py) ─────────────────────────────────

INFURA_URL = os.getenv("RPC_URL")  # or your Infura URL
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")  # if using Etherscan

def fetch_transactions(address):
    # example using Etherscan:
    url = (
      f"https://api.etherscan.io/api"
      f"?module=account&action=txlist"
      f"&address={address}"
      f"&startblock=0&endblock=99999999"
      f"&sort=asc&apikey={ETHERSCAN_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "1":
        st.error(f"Etherscan error: {data.get('message')}")
        return []
    return data.get("result", [])

def draw_graph(address):
    logs = fetch_transactions(address)
    G = nx.DiGraph()
    for tx in logs:
        frm = tx.get("from"); to = tx.get("to")
        if frm and to:
            G.add_edge(frm, to)
    return G

def send_telegram(address):
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=f"🚨 New Bounty Submission!\nAddress: {address}"
    )

# ─── Streamlit App ────────────────────────────────────────────────────────────

st.set_page_config(page_title="TRACE Alpha")

tabs = st.tabs(["Wallet Inspector", "Graph View", "Submit Bounty"])

with tabs[0]:
    addr = st.text_input("Enter wallet address:")
    if addr:
        txs = fetch_transactions(addr)
        st.dataframe(txs)

with tabs[1]:
    addr = st.text_input("Enter wallet for graph:")
    if addr:
        G = draw_graph(addr)
        plt.figure(figsize=(5,5))
        nx.draw(G, with_labels=True)
        st.pyplot(plt)

with tabs[2]:
    baddr = st.text_input("Suspicious address:")
    if st.button("Submit Bounty") and baddr:
        send_telegram(baddr)
        st.success("Bounty submitted! Telegram alert sent.")
