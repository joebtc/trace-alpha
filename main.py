import streamlit as st
from utils import fetch_transactions, draw_graph, send_telegram
import matplotlib.pyplot as plt

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
        st.pyplot(plt.figure(figsize=(5,5)))
        nx.draw(G, with_labels=True)
        st.pyplot(plt)

with tabs[2]:
    baddr = st.text_input("Suspicious address:")
    if st.button("Submit Bounty") and baddr:
        send_telegram(baddr)
        st.success("Bounty submitted! Telegram alert sent.")
