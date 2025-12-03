import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Edit later!!!!!!!
# -------------------------------------------------------------------
news_df = pd.read_csv("gold-dataset.csv")
news_df["Dates"] = [c.replace("-","/") for c in news_df["Dates"]]
news_df["Dates"] = pd.to_datetime(news_df["Dates"],errors='coerce', dayfirst=True)
news_df["Price Sentiment"] = news_df["Price Sentiment"].str.strip().str.lower()

# Map sentiment to numeric signal: +1 = long (positive), -1 = short (negative)
sentiment_map = {"positive": 1, "negative": -1}
news_df = news_df[news_df["Price Sentiment"].isin(sentiment_map.keys())]
news_df["SentimentScore"] = news_df["Price Sentiment"].map(sentiment_map)


# Price
# -------------------------------------------------------------------
gold = gold = pd.read_excel('Gold_Prices.xlsx')
gold["Name"] = pd.to_datetime(gold["Name"],errors='coerce', dayfirst=True)


# 3-day return
# -------------------------------------------------------------------
gold["FutureClose"] = gold["US dollar"].shift(-3)
gold["FutureReturn"] = (gold["FutureClose"] - gold["US dollar"]) / gold["US dollar"]


# Match price to signals
# -------------------------------------------------------------------
merged = pd.merge(
    news_df.set_index("Dates"),
    gold.set_index("Name"),
    left_index=True,
    right_index=True,
    how="inner"
)

merged = merged.dropna(subset=["FutureReturn"])

merged["PriceDirection"] = np.sign(merged["FutureReturn"])  # +1 up, -1 down

merged["Correct"] = (merged["SentimentScore"] == merged["PriceDirection"])


# Autistic stats
# -------------------------------------------------------------------
total_signals = len(merged)
accuracy = merged["Correct"].mean() if (total_signals > 0) else (np.nan)

pos = merged[merged["SentimentScore"] == 1]
neg = merged[merged["SentimentScore"] == -1]

stats = {
    "total_articles": total_signals,
    "accuracy_overall": accuracy,
    "positive": len(pos),
    "negative": len(neg),
    "positive_accuracy": pos["Correct"].mean() if len(pos) > 0 else np.nan,
    "negative_accuracy": neg["Correct"].mean() if len(neg) > 0 else np.nan,
    "avg_3_day_return_after_positive": pos["FutureReturn"].mean() if len(pos) > 0 else np.nan,
    "avg_3_day_return_after_negative": neg["FutureReturn"].mean() if len(neg) > 0 else np.nan,
}

print("=== Stats ===")
for k, v in stats.items():
    print(f"{k}:", '%.4f'%v) if not type(v) == type(0) else print(f"{k}:", v)
print()

# Frame
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6))


ax.plot(gold["Name"], gold["US dollar"], label="Gold Close Price")


article_dates = merged.index
article_prices = merged["US dollar"]


pos_mask = merged["SentimentScore"] == 1
ax.scatter(
    article_dates[pos_mask],
    article_prices[pos_mask],
    marker="^",      
    s=100,
    color="green",
    label="Positive news (long)"
)


neg_mask = merged["SentimentScore"] == -1
ax.scatter(
    article_dates[neg_mask],
    article_prices[neg_mask],
    marker="v",   
    s=100,
    color="red",
    label="Negative news (short)"
)
##-------------------------------------------
ax.set_title("Random Gold Price History with News-Based Long/Short Signals")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()
