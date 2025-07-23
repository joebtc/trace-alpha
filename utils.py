import requests

def get_labels(address):
    labels = []
    # 1) Moralis (ERC-20 patterns, known bridges)
    moralis_key = os.getenv("MORALIS_API_KEY")
    if moralis_key:
        url = f"https://deep-index.moralis.io/api/v2/{address}/balance"
        res = requests.get(url, headers={"X-API-Key": moralis_key})
        if res.ok:
            labels.append("Moralis OK")
    # 2) Flipside (SQL query for known CEX wallets)
    flipside_key = os.getenv("FLIPSIDE_API_KEY")
    if flipside_key:
        sql = """
          SELECT label 
          FROM wallet_labels 
          WHERE wallet_address = LOWER('%s')
        """ % address
        res = requests.post(
            "https://api.flipsidecrypto.com/api/v2/queries",
            headers={"x-api-key": flipside_key},
            json={"sql": sql, "ttlMinutes": 5}
        )
        if res.ok and res.json().get("data"):
            labels.append(res.json()["data"][0]["label"])
    return labels or ["unlabeled"]
