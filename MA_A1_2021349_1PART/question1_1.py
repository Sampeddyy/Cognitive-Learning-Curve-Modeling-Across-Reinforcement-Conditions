import pandas as pd

# Load the dataset
input_file_path = r'C:\Users\Gungun shah\Downloads\LM_A1_2021349\LM_A1_Winter_ParticipantSheets.xlsx'  # Input Excel file
output_file_path = r'C:\Users\Gungun shah\Downloads\LM_A1_2021349\answer1_1.xlsx'  # Output Excel file

# Step 1: Read all sheets (one sheet per participant) from the Excel file
participant_sheets = pd.read_excel(input_file_path, sheet_name=None)  # Reads all sheets into a dictionary

# Step 2: Calculate the global average SCR across all participants
global_avg_scr = 0  # Initialize global average SCR
total_participants = len(participant_sheets)  # Total number of participants

# Loop through each participant's sheet to calculate their average SCR
for sheet_name, participant_data in participant_sheets.items():
    # Calculate the average SCR for the current participant
    participant_avg_scr = participant_data['sqrtSCRUS'].mean()
    # Add the participant's average SCR to the global average
    global_avg_scr += participant_avg_scr

# Calculate the global average SCR
global_avg_scr /= total_participants  # Divide by the number of participants to get the global average

# Step 3: Normalize the SCR values for each participant
normalized_data = {}  # Dictionary to store normalized SCR values for each participant

# Loop through each participant's sheet again to normalize their SCR values
for sheet_name, participant_data in participant_sheets.items():
    # Step 1: Calculate the average SCR for the current participant
    participant_avg_scr = participant_data['sqrtSCRUS'].mean()
    
    # Step 2: Subtract the participant's average SCR from their individual SCR values
    participant_data['CenteredSCR'] = participant_data['sqrtSCRUS'] - participant_avg_scr
    
    # Step 3: Adjust the scores by adding the global average SCR
    participant_data['NormalizedSCR'] = participant_data['CenteredSCR'] + global_avg_scr
    
    # Store the normalized SCR values for the current participant
    normalized_data[sheet_name] = participant_data['NormalizedSCR'].tolist()

# Step 4: Save the normalized data to a new Excel file
normalized_df = pd.DataFrame(normalized_data)
normalized_df.to_excel(output_file_path, index=False)

print(f"Normalized SCR data saved to: {output_file_path}")
