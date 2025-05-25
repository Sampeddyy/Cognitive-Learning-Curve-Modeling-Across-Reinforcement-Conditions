import os
import math
import pandas as pd
import numpy as np

# Define file path
file_path = r"C:\Users\Gungun shah\Downloads\LM_A1_2021349\LM_A1_Winter_ParticipantSheets.xlsx"

# Read the Excel file (assuming each sheet is a participant's data)
xl = pd.ExcelFile(file_path)

# Initialize an empty list to store results
results = []

# Process each participant sheet
for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)  # Read participant sheet
    
    # Ensure necessary columns exist
    required_columns = {'ParticipantID', 'CSCategory', 'CS', 'Phase', 'CSCount', 'sqrtSCRUS'}
    if not required_columns.issubset(df.columns):
        continue  # Skip if columns are missing
    
    # Normalize sqrtSCRUS within participant
    mean_scr = df['sqrtSCRUS'].mean()
    std_scr = df['sqrtSCRUS'].std()
    df['NormalizedSCR'] = (df['sqrtSCRUS'] - mean_scr) / std_scr if std_scr != 0 else df['sqrtSCRUS']
    
    # Group data by CSCategory and CS, then compute mean and SEM
    grouped = df.groupby(['CSCategory', 'CS'])['NormalizedSCR']
    summary = grouped.agg(MeanNormalized='mean', SEM=lambda x: np.std(x, ddof=1) / math.sqrt(len(x)))
    
    # Store results with ParticipantID
    summary['ParticipantID'] = df['ParticipantID'].iloc[0]  # Extract Participant ID
    results.append(summary.reset_index())

# Combine results from all participants
final_df = pd.concat(results, ignore_index=True)

# Round values for better readability
final_df[['MeanNormalized', 'SEM']] = final_df[['MeanNormalized', 'SEM']].round(3)

# Save output to a structured Excel file
output_path = r"C:\Users\Gungun shah\Downloads\answer1_2.xlsx"
final_df.to_excel(output_path, index=False)

print(f"Processed data saved to: {output_path}")
