# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import os  # For file path operations

# Define the file path to the dataset
file_directory = r'C:\Users\Gungun shah\Downloads\LM_A1_2021349'  # Directory where the file is located
file_name = 'LM_A1_Winter.xlsx'  # Name of the Excel file
input_file_path = os.path.join(file_directory, file_name)  # Full path to the file

# Check if the file exists
if not os.path.exists(input_file_path):
    print(f"Error: The file '{input_file_path}' does not exist.")
    print("Please verify the file path and ensure the file is in the correct location.")
else:
    print(f"File found at: {input_file_path}")

    # Load the dataset into a pandas DataFrame
    try:
        experiment_data = pd.read_excel(input_file_path)  # Load the Excel file into a DataFrame
        print("File loaded successfully!")
    except Exception as e:
        print(f"Error loading the file: {e}")

    # Define the output file path for the new Excel file
    output_file_name = 'LM_A1_Winter_ParticipantSheets.xlsx'  # Name of the output Excel file
    output_file_path = os.path.join(file_directory, output_file_name)  # Full path to the output file

    # Create an Excel writer object to write multiple sheets
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as excel_writer:  # Use 'openpyxl' as the engine
        # Iterate through each unique participant ID in the dataset
        for participant in experiment_data['ParticipantID'].unique():  # Loop through each participant
            # Filter the dataset to include only the current participant's data
            participant_trials = experiment_data[experiment_data['ParticipantID'] == participant]  # Filter rows for the participant
            
            # Create a sheet name for the current participant
            sheet_name = f'Participant_{participant}'  # Sheet name format: "Participant_X"
            
            # Write the participant's data to the corresponding sheet in the Excel file
            participant_trials.to_excel(excel_writer, sheet_name=sheet_name, index=False)  # Write to Excel without row indices

    # Print a confirmation message
    print(f"Excel file with separate sheets for each participant has been created at: {output_file_path}")