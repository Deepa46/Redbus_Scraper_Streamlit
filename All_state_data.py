import pandas as pd
import os

# List of CSV files to be merged
csv_files = [
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\AP_data.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\assam_astc.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\kadamba.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\kerala_data.csv",
     r"C:\Users\yuvar\PycharmProjects\RedBus_Project\punjab.csv" ,
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\telugana.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\westbengal.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\SouthBengal.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\HP_hrtc.csv",
    r"C:\Users\yuvar\PycharmProjects\RedBus_Project\Bihar_bsrtc.csv"
]

# Create an empty list to store dataframes
dataframes = []

# Read each CSV file and append to the list
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate all dataframes into one
merged_df = pd.concat(dataframes)

# Save the merged dataframe to a new CSV file
merged_df.to_csv("All_state_data.csv", index=False)

print("CSV files have been successfully merged ")
