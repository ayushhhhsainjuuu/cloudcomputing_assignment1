import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "data/All_Diets.csv"

OUT_DIR = "outputs"
CHART_DIR = "charts"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)

def safe_ratio(numer, denom):
    denom = denom.replace(0, np.nan)
    return numer / denom

def main():
    df = pd.read_csv(CSV_PATH)

    df["Diet_type"] = df["Diet_type"].astype(str).str.strip()
    df["Cuisine_type"] = df["Cuisine_type"].astype(str).str.strip().str.lower()
    df["Recipe_name"] = df["Recipe_name"].astype(str).str.strip()

    macro_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
    for c in macro_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df[macro_cols] = df[macro_cols].fillna(df[macro_cols].mean())

    df["Protein_to_Carbs_ratio"] = safe_ratio(df["Protein(g)"], df["Carbs(g)"])
    df["Carbs_to_Fat_ratio"] = safe_ratio(df["Carbs(g)"], df["Fat(g)"])

    avg_macros = df.groupby("Diet_type")[macro_cols].mean()
    avg_macros.to_csv("outputs/avg_macros_by_diet.csv")

    top5 = (
        df.sort_values(["Diet_type", "Protein(g)"], ascending=[True, False])
        .groupby("Diet_type")
        .head(5)
    )
    top5.to_csv("outputs/top5_protein_by_diet.csv", index=False)

    cuisine_counts = (
        df.groupby(["Diet_type", "Cuisine_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["Diet_type", "count"], ascending=[True, False])
    )
    cuisine_counts.to_csv("outputs/common_cuisines_by_diet.csv", index=False)

    # BAR CHART
    plt.figure(figsize=(12,6))
    avg_macros.plot(kind="bar")
    plt.title("Average Macronutrients by Diet Type")
    plt.tight_layout()
    plt.savefig("charts/avg_macros_bar.png")
    plt.close()

    # HEATMAP
    plt.figure(figsize=(10,6))
    sns.heatmap(avg_macros, cmap="viridis")
    plt.title("Heatmap of Avg Macronutrients")
    plt.tight_layout()
    plt.savefig("charts/macros_heatmap.png")
    plt.close()

    # SCATTER
    plt.figure(figsize=(10,6))
    plt.scatter(df["Protein(g)"], df["Carbs(g)"])
    plt.xlabel("Protein (g)")
    plt.ylabel("Carbs (g)")
    plt.title("Protein vs Carbs")
    plt.tight_layout()
    plt.savefig("charts/top5_scatter.png")
    plt.close()

    print("Task 1 Complete.")

if __name__ == "__main__":
    main()

