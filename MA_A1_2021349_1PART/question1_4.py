import pandas as pd
import numpy as np
from statsmodels.stats.diagnostic import lilliefors
import scipy.stats as stats

# Load the dataset
file_path = r"C:\Users\Gungun shah\Downloads\LM_A1_Winter.xlsx"
df = pd.read_excel(file_path)

# Ensure correct column names
expected_columns = ["ParticipantID", "CSCategory", "CS", "Phase", "CSCount", "normalizedSCR"]
df.columns = expected_columns

def compare_scr_phase2(cs_category, phase2_data):
    phase2_data = phase2_data[(phase2_data['Phase'] == 'Phase2') & (phase2_data['CSCategory'] == cs_category)]
    phase2_data = phase2_data.dropna(subset=['normalizedSCR'])
    cs_plus_scr = phase2_data[phase2_data['CS'] == 'CS+']['normalizedSCR']
    cs_minus_scr = phase2_data[phase2_data['CS'] == 'CS-']['normalizedSCR']
    
    min_trials = min(len(cs_plus_scr), len(cs_minus_scr))
    cs_plus_scr = cs_plus_scr.sample(n=min_trials, random_state=42)
    cs_minus_scr = cs_minus_scr.sample(n=min_trials, random_state=42)
    
    print(f"For {cs_category} Faces: CS+ trials: {len(cs_plus_scr)}, CS- trials: {len(cs_minus_scr)}")
    
    stat, p = lilliefors(cs_plus_scr - cs_minus_scr)
    if p < 0.05:
        stat, p_value = stats.wilcoxon(cs_plus_scr, cs_minus_scr)
    else:
        stat, p_value = stats.ttest_rel(cs_plus_scr, cs_minus_scr)

    return stat, p_value

# Define CS categories
cs_categories = ['Angry', 'Neutral', 'Happy']

# Run tests for each category
data = df  # Reference the dataseta
for cs_category in cs_categories:
    stat, p_value = compare_scr_phase2(cs_category, data)
    if np.isnan(stat) or np.isnan(p_value):
        print(f'For {cs_category} Faces, insufficient data or mismatched group sizes.')
    else:
        print(f'For {cs_category} Faces, Test Statistic: {stat}, p-value: {p_value}')
