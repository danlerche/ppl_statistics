from datetime import datetime
import pandas as pd

# Ask the user to input a date
date_input = input("Enter the date for this report (YYYY-MM-DD): ")

# Optional: validate and parse it
try:
    date_value = datetime.strptime(date_input, "%Y-%m-%d").date()
except ValueError:
    raise ValueError("Date format must be YYYY-MM-DD")

df = pd.read_csv("circ.csv", delimiter=";")

def merge_rows(df, rows_to_merge, new_name):
    selected_rows = df[df["Item Type"].isin(rows_to_merge)]
    summed = selected_rows[["Checkouts", "Renewals"]].sum()
    new_row = pd.DataFrame([{
        "Item Type": new_name,
        "Checkouts": summed["Checkouts"],
        "Renewals": summed["Renewals"]
    }])
    df = df[~df["Item Type"].isin(rows_to_merge)]
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Merge rows
df = merge_rows(df, ["Children's Book", "Children's Book No Requests"], "children")
df = merge_rows(df, ["Adult DVD", "Children's DVD"], "dvd")
df = merge_rows(df, ["Children's Magazine", "Adult Magazine"], "magazine")
df = merge_rows(df, ["Book Club Set", "Adult Book", "Homebound Internal Collection"], "adult")

# Remove all "Library of Things" rows
rows_to_delete = [
    "Library of Things 1 Week",
    "Library of Things 2 Weeks",
    "Library of Things 3 Weeks ",
    "Library of Things 4 Weeks"
]
df = df[~df["Item Type"].isin(rows_to_delete)]

# Rename 'Young Adult Book' to 'Young Adult'
df.loc[df["Item Type"] == "Young Adult Book", "Item Type"] = "young_adult"
# Rename 'Interlibrary Loan' to 'ILL'
df.loc[df["Item Type"] == "Interlibrary Loan", "Item Type"] = "ill"
# Rename 'Audio Book' to 'Audiobook'
df.loc[df["Item Type"] == "Audio Book", "Item Type"] = "audiobook"
# Rename 'Talking Book' to 'Accessible'
df.loc[df["Item Type"] == "Talking Book", "Item Type"] = "accessible"

# Rename columns for the csv upload app
df = df.rename(columns={"Item Type": "circ_stat_type"})
df = df.rename(columns={"Checkouts": "checkouts"})
df = df.rename(columns={"Renewals": "renewals"})

# Add date column
df.insert(0, "date", date_value)
# Sort and export
df = df.sort_values("circ_stat_type").reset_index(drop=True)
df.to_csv("circ_updated.csv", index=False, sep=";")

print("Final CSV saved as circ_updated.csv with merged and cleaned data.")

#lot_df = pd.read_csv("lot_circ.csv", delimiter=";")
