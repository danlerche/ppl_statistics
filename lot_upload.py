import pandas as pd
from datetime import datetime

# Prompt for a date
date_input = input("Enter the date for this report (YYYY-MM-DD): ")

# Validate and parse date
try:
    date_value = datetime.strptime(date_input, "%Y-%m-%d").date()
except ValueError:
    raise ValueError("Date format must be YYYY-MM-DD")

# Load the CSV file
df = pd.read_csv("lot_circ.csv", delimiter=";")

# Rename LOTNINTENDO to video_game
df.loc[df["Collection Code"] == "LOTNINTENDO", "Collection Code"] = "video_game"

# Separate video_game and the rest
video_game_row = df[df["Collection Code"] == "video_game"]
other_rows = df[df["Collection Code"] != "video_game"]

# Sum the rest and label as 'lot'
lot_sums = other_rows[["Checkouts", "Renewals"]].sum()
lot_row = pd.DataFrame([{
    "Collection Code": "lot",
    "Checkouts": lot_sums["Checkouts"],
    "Renewals": lot_sums["Renewals"]
}])

# Combine rows
final_df = pd.concat([video_game_row, lot_row], ignore_index=True)
final_df = final_df.sort_values("Collection Code").reset_index(drop=True)

# Add date column
final_df.insert(0, "date", date_value)

# Rename columns
final_df = final_df.rename(columns={
    "Collection Code": "circ_stat_type",
    "Checkouts": "checkouts",
    "Renewals": "renewals"
})

# Save to CSV
final_df.to_csv("lot_updated.csv", index=False, sep=";")

print("Saved file with updated headers and data to collection_updated.csv")