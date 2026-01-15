import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
#  Function: Two-Candle Chart
# -----------------------------
def make_chart(title, labels, current, previous, filename, show_pct=True):
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, previous, width, label='Previous', color='#FFA726')
    rects2 = ax.bar(x + width/2, current, width, label='Current', color='#42A5F5')

    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha='right')
    ax.legend()

    # Show % difference labels
    if show_pct:
        for i, (c, p) in enumerate(zip(current, previous)):
            if p == 0:
                change = 0
            else:
                change = ((c - p) / p) * 100
            color = "green" if change >= 0 else "red"
            ax.text(x[i], max(c, p) + max(current)*0.03,
                    f"{change:+.1f}%", ha='center', color=color, fontsize=10, fontweight='bold')

    ax.set_ylabel("Count")
    ax.set_xlabel("Categories")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"✅ Saved: {filename}")


# ---------------------------------------------------
# 1️⃣  Key Highlights
# ---------------------------------------------------
labels = ["Active Users", "Views", "Sessions", "New Users"]
current = [84, 550, 167, 79]
previous = [70, 344, 145, 69]  # estimated previous based on growth %
make_chart("Key Highlights (BCS 14 Days)", labels, current, previous, "BCS_KeyHighlights.png")


# ---------------------------------------------------
# 2️⃣  Traffic Sources (Sessions)
# ---------------------------------------------------
labels = ["Direct", "Organic Search", "Unassigned", "Organic Social"]
current = [99, 64, 15, 2]
previous = [87, 55, 15, 1]
make_chart("Traffic Sources", labels, current, previous, "BCS_TrafficSources.png")


# ---------------------------------------------------
# 3️⃣  Active Users by Country
# ---------------------------------------------------
labels = ["United Kingdom", "United States", "Germany", "Ireland", "Australia", "Canada", "Spain"]
current = [53, 15, 7, 2, 1, 1, 1]
previous = [47, 13, 7, 2, 1, 1, 1]
make_chart("Active Users by Country", labels, current, previous, "BCS_CountryBreakdown.png")


# ---------------------------------------------------
# 4️⃣  Top Pages (Views)
# ---------------------------------------------------
labels = [
    "Same Day Luxury Flowers",
    "Fresh Flower Delivery",
    "User Login",
    "Funeral & Sympathy",
    "Delivery Info",
    "Shopping Basket",
    "Wedding & Bridal"
]
current = [144, 91, 54, 28, 16, 19, 12]
previous = [92, 65, 52, 20, 11, 5, 10]
make_chart("Top Pages by Views", labels, current, previous, "BCS_TopPages.png")


# ---------------------------------------------------
# 5️⃣  User Engagement (Event Count)
# ---------------------------------------------------
labels = ["Page Views", "Session Starts", "First Visits"]
current = [550, 166, 79]
previous = [344, 145, 69]
make_chart("User Engagement", labels, current, previous, "BCS_UserEngagement.png")

print("\n🎉 All charts generated successfully!")
