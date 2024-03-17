import matplotlib.pyplot as plt
import pandas as pd
import json

# Assuming your data is stored in a variable named 'data'
# Extracting team names and win-loss information
teams = set()
team_wins = {}
team_losses = {}

with open("2023_data.json", "r") as fn:
    data = json.load(fn)

for year_data in data:
    for game_data in year_data['data']:
        for round_num, round_data in game_data.items():
            for round in round_data:
                for team_data in round["teams"]:
                    team_name = team_data['name']
                    teams.add(team_name)
                    if team_name not in team_wins:
                        team_wins[team_name] = 0
                        team_losses[team_name] = 0
                    
                    if team_data['won']:
                        team_wins[team_name] += 1
                    else:
                        team_losses[team_name] += 1

# Calculating win-loss ratio
win_loss_ratio = {team: team_wins[team] / (team_wins[team] + team_losses[team]) for team in teams}

# Converting the dictionary to a DataFrame for easier plotting
win_loss_df = pd.DataFrame(list(win_loss_ratio.items()), columns=['Team', 'Win-Loss Ratio'])

# Sorting DataFrame by Win-Loss Ratio
win_loss_df = win_loss_df.sort_values(by='Win-Loss Ratio', ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
plt.barh(win_loss_df['Team'], win_loss_df['Win-Loss Ratio'], color='skyblue')
plt.xlabel('Win-Loss Ratio')
plt.title('Win-Loss Ratio for Each AFL Team')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
