from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import pandas as pd
import json

with open("2023_data.json", "r") as fn:
    data = json.load(fn)


# Assuming your data is stored in a variable named 'data'
rows = []

for year_data in data:
    for game_data in year_data['data']:
        for round_num, round_data in game_data.items():
            for game_round in round_data:
                for team_data in game_round["teams"]:
                    team_name = team_data['name']
                    won = team_data['won']
                    venue = game_round['venue']
                    rows.append({'Team': team_name, 'Won': won, 'Venue': venue})

# Create DataFrame
df = pd.DataFrame(rows)
import seaborn as sns
import matplotlib.pyplot as plt

# Calculate total games played at each venue
venue_counts = df['Venue'].value_counts()

# Calculate frequency of wins for each team at each stadium
win_frequency = df.groupby(['Venue', 'Team']).size().unstack(fill_value=0)

# Normalize the data
normalized_data = win_frequency.div(venue_counts, axis=0)

# Create countplot
plt.figure(figsize=(12, 8))
sns.barplot(data=normalized_data.reset_index().melt(id_vars='Venue'), x='Venue', y='value', hue='Team', palette='colorblind')
plt.title('Normalized Frequency of Wins for Each Team at Each Stadium')
plt.xlabel('Stadium')
plt.ylabel('Normalized Frequency of Wins')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
