import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Step 1: Load and Prepare Data ------------------
df = pd.read_csv("bayc_holdtime_data.csv")
df["blockTimestamp"] = pd.to_datetime(df["blockTimestamp"])
df = df.sort_values(by=["tokenId", "blockTimestamp"]).reset_index(drop=True)

# ------------------ Step 2: Calculate Hold Times ------------------
records = []

for token_id, group in df.groupby("tokenId"):
    group = group.sort_values("blockTimestamp").reset_index(drop=True)
    for i in range(len(group) - 1):
        current_holder = group.loc[i, "to"]
        next_sender = group.loc[i + 1, "from"]
        received_time = group.loc[i, "blockTimestamp"]
        sent_time = group.loc[i + 1, "blockTimestamp"]

        if current_holder.lower() == next_sender.lower():
            hold_time_days = (sent_time - received_time).total_seconds() / (3600 * 24)
            records.append({
                "tokenId": token_id,
                "holder": current_holder,
                "received_time": received_time,
                "sent_time": sent_time,
                "hold_time_days": hold_time_days
            })

hold_df = pd.DataFrame(records)
hold_df.to_csv("nft_holder_hold_times.csv", index=False)

# ------------------ Step 3: Average Hold Time Per Wallet ------------------
avg_hold = hold_df.groupby("holder")["hold_time_days"].mean().reset_index()
avg_hold.columns = ["holder", "avg_hold_time_days"]

# Count number of tokens held
nft_counts = hold_df.groupby("holder").size().reset_index(name="num_tokens")
avg_hold = avg_hold.merge(nft_counts, on="holder")

# ------------------ Step 4: Classify Wallets ------------------
def classify(holder_row):
    if holder_row["num_tokens"] >= 3 and holder_row["avg_hold_time_days"] < 1:
        return "Flipper"
    elif holder_row["avg_hold_time_days"] >= 7:
        return "Collector"
    else:
        return "Swing Trader"

avg_hold["label"] = avg_hold.apply(classify, axis=1)
avg_hold.to_csv("holder_classification.csv", index=False)

# ------------------ Step 5: Label Summary Statistics ------------------
label_summary = avg_hold.groupby("label").agg(
    count=("holder", "count"),
    avg_hold_time_days=("avg_hold_time_days", "mean")
).reset_index()

label_summary["percentage"] = (label_summary["count"] / label_summary["count"].sum() * 100).round(2)
label_summary.to_csv("holder_type_summary.csv", index=False)

print("\n📊 Holder Type Summary:")
print(label_summary.to_string(index=False))

# ------------------ Step 6: Plot Hold Time Distribution ------------------
plt.figure(figsize=(10, 6))
plt.hist(hold_df["hold_time_days"], bins=200, edgecolor='black')
plt.xlabel("Hold Time (days)")
plt.ylabel("Number of Transfers")
plt.title("Distribution of NFT Hold Times")
plt.grid(True)
plt.xlim(0, 200)
plt.tight_layout()
plt.savefig("hold_time_distribution.png")
plt.show()

print("\n✅ Analysis complete. CSVs and histogram saved.")