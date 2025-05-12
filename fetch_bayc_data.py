import requests
import pandas as pd

# ------------------ GraphQL Setup ------------------
GRAPHQL_URL = "https://api.studio.thegraph.com/query/110146/bayc-holdtime/version/latest"

def fetch_all_transfers():
    all_transfers = []
    last_tx = ""
    batch_size = 1000
    batch_num = 0

    while True:
        filter_clause = f'transactionHash_gt: "{last_tx}"' if last_tx else ""
        query = f"""
        {{
          transfers(first: {batch_size}, orderBy: transactionHash, orderDirection: asc, where: {{{filter_clause}}}) {{
            tokenId
            from
            to
            blockTimestamp
            transactionHash
          }}
        }}
        """
        response = requests.post(GRAPHQL_URL, json={"query": query})

        try:
            json_data = response.json()
        except Exception as e:
            print(f"Failed to parse JSON in batch {batch_num}: {e}")
            print(response.text)
            break

        if "data" not in json_data or "transfers" not in json_data["data"]:
            print(f"Invalid response in batch {batch_num}:")
            print(json_data)
            break

        data = json_data["data"]["transfers"]
        if not data:
            print("All data fetched!")
            break

        all_transfers.extend(data)
        last_tx = data[-1]["transactionHash"]
        batch_num += 1
        print(f"Fetched batch {batch_num}, total records: {len(all_transfers)}")

    return pd.DataFrame(all_transfers)

# Fetch all transfer data
df = fetch_all_transfers()

# Convert timestamps
df["blockTimestamp"] = pd.to_datetime(pd.to_numeric(df["blockTimestamp"]), unit="s")

# ------------------ Save Locally ------------------
df.to_csv("bayc_holdtime_data.csv", index=False)
print("All data saved to bayc_holdtime_data.csv")