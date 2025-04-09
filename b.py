import pandas as pd

# Load real dataset
df2020 = pd.read_csv("final_daily_rainfall_2020.csv")

# Extract unique district-mandal pair
unique_pairs = df2020[['District', 'Mandal']].drop_duplicates().sort_values(by=['District', 'Mandal']).reset_index(drop=True)

# Add placeholder column
placeholder_list = []
for i, (district, group) in enumerate(unique_pairs.groupby("District"), start=1):
    for j, (_, row) in enumerate(group.iterrows(), start=1):
        placeholder = f"Mandal_District_{i}_{j}"
        placeholder_list.append({
            'Placeholder': placeholder,
            'District': row['District'],
            'Mandal': row['Mandal']
        })

# Create and save mapping
lookup_df = pd.DataFrame(placeholder_list)
lookup_df.to_csv("manual_lookup.csv", index=False)
print("✅ manual_lookup.csv created with placeholder → real name mapping.")
