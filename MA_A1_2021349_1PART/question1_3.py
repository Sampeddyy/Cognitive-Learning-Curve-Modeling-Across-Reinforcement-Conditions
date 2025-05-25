import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"C:\Users\Gungun shah\Downloads\LM_A1_Winter.xlsx"
df = pd.read_excel(file_path)

# Ensure correct column names
expected_columns = ["ParticipantID", "CS Category", "CS", "Phase", "CSCount", "sqrtSCRUS"]
df.columns = expected_columns

# Define categories and colors
cs_categories = {"Angry": "violet", "Neutral": "blue", "Happy": "green"}
line_styles = {"CS+": "-", "CS-": "--"}

# Filter Phase 2 Data
phase2_data = df[df["Phase"] == "Phase2"]

# Create a figure with 3x1 subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12), sharex=True)

for idx, (category, color) in enumerate(cs_categories.items()):
    ax = axes[idx]
    for cs_type, line_style in line_styles.items():
        subset = df[(df["CS Category"] == category) & (df["CS"] == cs_type)]
        mean_scr = subset.groupby("CSCount")["sqrtSCRUS"].mean()
        sem_scr = subset.groupby("CSCount")["sqrtSCRUS"].sem()
        
        # Plot with error bars
        ax.errorbar(mean_scr.index, mean_scr, yerr=sem_scr, fmt=line_style, color=color, label=f"{cs_type}")
    
    # Mark Phase 2 start and end
    ax.axvline(x=3, color='black', linestyle='dotted')
    ax.axvline(x=9, color='black', linestyle='dotted')
    
    ax.set_title(f"{category} CS Category")
    ax.set_ylabel("SCR Response (sqrt)")
    ax.legend()
    ax.grid(True)

axes[-1].set_xlabel("Trial Number")
plt.suptitle("SCR Responses for CS+ and CS- Conditions across Categories")
plt.tight_layout()
plt.show()
