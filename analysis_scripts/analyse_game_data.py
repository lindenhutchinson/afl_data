import pandas as pd

# Load DataFrame from CSV file
df = pd.read_csv("football_data.csv")

# Correlation analysis
# correlation_matrix = df.corr()
# print("\nCorrelation Matrix:")
# print(correlation_matrix)

from scipy.stats import pearsonr

# Calculate Pearson correlation coefficient and p-value for relevant columns
correlation_coefficient, p_value = pearsonr(df['Final Score'], df['Won'])

# Set significance level (alpha)
alpha = 0.05

# Check if the correlation is statistically significant
if p_value < alpha:
    print(f"There is a statistically significant correlation between Final Score and Margin (Pearson correlation coefficient = {correlation_coefficient:.2f}, p-value = {p_value:.2f}).")
else:
    print(f"There is no statistically significant correlation between Final Score and Margin (Pearson correlation coefficient = {correlation_coefficient:.2f}, p-value = {p_value:.2f}).")

# from scipy.stats import f_oneway

# # Perform ANOVA test
# result = f_oneway(*[df[df['Venue'] == venue]['Final Score'] for venue in df['Venue'].unique()])

# # Set significance level (alpha)
# alpha = 0.05

# # Check if the p-value is less than alpha to determine statistical significance
# if result.pvalue < alpha:
#     print(f"There is a statistically significant relationship between Final Score and Venue (p-value = {result.pvalue:.2f}).")
# else:
#     print(f"There is no statistically significant relationship between Final Score and Venue (p-value = {result.pvalue:.2f}).")

# # There is a statistically significant correlation between Final Score and Margin (Pearson correlation coefficient = 0.13, p-value = 0.00).