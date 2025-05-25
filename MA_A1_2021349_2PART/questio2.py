import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kruskal, mannwhitneyu
import seaborn as sns

# Load the data from the Excel file
file_path = r"C:\Users\Gungun shah\Downloads\LM_A1_2021349\MA_A1_2021349_2PART\LM_A1_Winter.xlsx"
data = pd.read_excel(file_path)

# Normalize SCR values
avg_scr_per_participant = data.groupby('ParticipantID')['sqrtSCRUS'].mean()
data['adjustedSCR'] = data.apply(lambda row: row['sqrtSCRUS'] - avg_scr_per_participant[row['ParticipantID']], axis=1)
overall_avg = avg_scr_per_participant.mean()
data['normalizedSCR'] = data['adjustedSCR'] + overall_avg

# Compute mean and SEM for each CS category
mean_sem_data = data.groupby(['CSCategory', 'CS', 'Phase', 'CSCount'])['normalizedSCR'].agg(['mean', 'sem']).reset_index()

# Filter data for Phase 2 and CS+
phase2_data = mean_sem_data[(mean_sem_data['Phase'] == 'Phase2') & (mean_sem_data['CS'] == 'CS+')]

# Compute learning rate (slope) for each participant in each CS category
learning_rates = []
for participant in data['ParticipantID'].unique():
    for category in ['Angry', 'Neutral', 'Happy']:
        participant_data = data[(data['ParticipantID'] == participant) & 
                                (data['CSCategory'] == category) & 
                                (data['Phase'] == 'Phase2') & 
                                (data['CS'] == 'CS+')]
        
        if len(participant_data) > 1:  # Ensure at least 2 trials
            x = participant_data['CSCount'].values
            y = participant_data['normalizedSCR'].values
            slope, _ = np.polyfit(x, y, 1)  # Fit line, extract slope
            learning_rates.append([participant, category, slope])
        else:
            learning_rates.append([participant, category, np.nan])  # Not enough data

# Save learning rates to a CSV file
learning_rates_df = pd.DataFrame(learning_rates, columns=['ParticipantID', 'CSCategory', 'LearningRate'])
learning_rates_df.to_csv(r"C:\Users\Gungun shah\Downloads\LM_A1_2021349\MA_A1_2021349_2PART\learning_rates.csv", index=False)

# Print confirmation
print("Learning rates saved to learning_rates.csv")

# Prepare for plotting
cs_categories = ['Angry', 'Neutral', 'Happy']
colors = {'Angry': 'violet', 'Neutral': 'blue', 'Happy': 'green'}
means = [phase2_data[phase2_data['CSCategory'] == cat]['mean'].mean() for cat in cs_categories]
sems = [phase2_data[phase2_data['CSCategory'] == cat]['sem'].mean() for cat in cs_categories]

# Create a bar plot for the mean rate of learning with error bars
plt.figure(figsize=(8, 6))
sns.barplot(x=cs_categories, y=means, errorbar="se", palette=[colors[cat] for cat in cs_categories])
plt.title('Mean Rate of Learning During Phase 2')
plt.xlabel('CS Category')
plt.ylabel('Mean Normalized SCR')
plt.show()

# Perform the Kruskal-Wallis test to compare the mean rate of learning across CS categories
statistic, p_value = kruskal(*[phase2_data[phase2_data['CSCategory'] == cat]['mean'] for cat in cs_categories])
print(f"\nKruskal-Wallis Test Results: Statistic = {statistic}, p-value = {p_value}")

# Perform post-hoc Mann-Whitney U tests for pairwise comparisons
post_hoc_results = []
for i in range(len(cs_categories)):
    for j in range(i + 1, len(cs_categories)):
        cs1, cs2 = cs_categories[i], cs_categories[j]
        statistic, p_value = mannwhitneyu(
            phase2_data[phase2_data['CSCategory'] == cs1]['mean'],
            phase2_data[phase2_data['CSCategory'] == cs2]['mean']
        )
        post_hoc_results.append((cs1, cs2, statistic, p_value))

print("\nPost-hoc Mann-Whitney U Test Results:")
for result in post_hoc_results:
    print(f"{result[0]} vs {result[1]}: Statistic = {result[2]}, p-value = {result[3]}")

# Conclusion based on the results
if p_value < 0.05:
    print("\nConclusion: There is a significant influence of emotions/faces on the rate of learning during Phase 2.")
else:
    print("\nConclusion: There is no significant influence of emotions/faces on the rate of learning during Phase 2.")
