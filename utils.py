import os, requests, networkx as nx
from telegram import Bot

def fetch_transactions(address):
    key = os.getenv('COVALENT_API_KEY')
    url = f"https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?key={key}"
    data = requests.get(url).json().get('data', {}).get('items', [])
    return data

def draw_graph(address):
    txs = fetch_transactions(address)
    G = nx.DiGraph()
    for tx in txs:
        G.add_edge(tx['from_address'], tx['to_address'])
    return G

def send_telegram(address):
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    bot.send_message(
        chat_id=os.getenv('TELEGRAM_CHAT_ID'),
        text=f"🚨 New Bounty Submission!\nAddress: {address}"
    )
