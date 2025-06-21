import pandas as pd

# Load both CSV files
df1 = pd.read_csv("circ_updated.csv", delimiter=";")
df2 = pd.read_csv("lot_updated.csv", delimiter=";")

# Combine them
combined_df = pd.concat([df1, df2], ignore_index=True)

# Optional: sort by circ_stat_type or date
combined_df = combined_df.sort_values(by=["date", "circ_stat_type"]).reset_index(drop=True)

# Export the combined file
combined_df.to_csv("combined_circ_stats.csv", index=False, sep=";")

print("Saved combined data to combined_circ_stats.csv")
