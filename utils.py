import os, requests, streamlit as st, networkx as nx
from telegram import Bot

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")

def fetch_transactions(address):
    st.text(f"🔑 Using Etherscan Key (first 6 chars): {ETHERSCAN_KEY[:6]}…")
    url = (
      f"https://api.etherscan.io/api"
      f"?module=account&action=txlist"
      f"&address={address}"
      f"&startblock=0&endblock=99999999"
      f"&sort=asc&apikey={ETHERSCAN_KEY}"
    )
    resp = requests.get(url)
    st.text(f"📡 Status: {resp.status_code}")
    st.text(f"📥 Resp snippet:\n{resp.text[:200]}")
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
