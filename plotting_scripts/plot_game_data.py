import seaborn as sns
import matplotlib.pyplot as plt


# Function to plot the distribution of final scores for each team
def plot_final_scores_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Final Score", hue="Team", multiple="stack", bins=20)
    plt.title("Distribution of Final Scores for Each Team")
    plt.xlabel("Final Score")
    plt.ylabel("Count")
    plt.legend(title="Team")
    plt.show()


# Function to plot the distribution of margins of victory/defeat
def plot_margin_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Margin", bins=20, kde=True)
    plt.title("Distribution of Margins of Victory/Defeat")
    plt.xlabel("Margin")
    plt.ylabel("Count")
    plt.show()


# Function to plot the relationship between quarters and final scores
def plot_quarter_scores_relationship(df):
    quarters = ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]
    plt.figure(figsize=(10, 6))
    for quarter in quarters:
        sns.scatterplot(data=df, x=quarter + " Goals", y="Final Score", hue="Team")
    plt.title("Relationship Between Quarter Scores and Final Scores")
    plt.xlabel("Goals in Quarter")
    plt.ylabel("Final Score")
    plt.legend(title="Team")
    plt.show()


import pandas as pd

# Load DataFrame from CSV file
df = pd.read_csv("football_data.csv")

# # Display the loaded DataFrame
# # print(df)
# plot_quarter_scores_relationship(df)
# plot_final_scores_distribution(df)
# plot_margin_distribution(df)


# import seaborn as sns
# import matplotlib.pyplot as plt

# # Set the size of the plot
# plt.figure(figsize=(12, 8))

# # Create a boxplot to visualize the relationship between final score and venue
# sns.boxplot(data=df, x='Venue', y='Final Score')
# plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
# plt.title('Relationship Between Final Score and Venue')
# plt.xlabel('Venue')
# plt.ylabel('Final Score')
# plt.tight_layout()  # Adjust layout to prevent clipping of labels
# plt.show()
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def get_smoothed_winrates(df):
    # Calculate win rate of each team at each venue
    win_rates = df.groupby(["Team", "Venue"])["Won"].mean().reset_index()

    # Calculate the number of games played by each team at each venue
    game_counts = df.groupby(["Team", "Venue"]).size().reset_index(name="Game Count")

    # Merge win rates and game counts
    win_rates = win_rates.merge(game_counts, on=["Team", "Venue"])

    # Set the pseudo-count for Laplace smoothing
    pseudo_count = 1

    # Apply Laplace smoothing to win rates
    win_rates["Win Rate"] = (
        win_rates["Won"] * win_rates["Game Count"] + pseudo_count
    ) / (win_rates["Game Count"] + 2 * pseudo_count)

    return win_rates


def get_winrates(df):
    win_rate_percentages = df.groupby(["Team", "Venue"])["Won"].mean().reset_index()
    win_rate_percentages["Win Rate"] = (
        win_rate_percentages["Won"] * 100
    )  # Convert win rate to percentage
    return win_rate_percentages


import seaborn as sns
import matplotlib.pyplot as plt


def plot_winrates_by_venue(df):
    import seaborn as sns


import matplotlib.pyplot as plt


def plot_winrates_by_venue(df):
    win_rates = get_smoothed_winrates(df)
    # Get unique venues
    venues = df["Venue"].unique()

    # Get unique teams
    teams = df["Team"].unique()

    # Create a color palette based on the teams' names
    team_colors = sns.color_palette("husl", len(teams))
    team_color_dict = {team: color for team, color in zip(teams, team_colors)}

    # Set the number of columns and rows for subplots
    num_cols = 2
    num_rows = (len(venues) - 1) // num_cols + 1

    # Set the size of each subplot
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Iterate over each venue
    for i, venue in enumerate(venues):
        # Filter data for the current venue
        venue_data = win_rates[win_rates["Venue"] == venue]

        # Sort win rates for the current venue
        sorted_data = venue_data.sort_values(by="Win Rate", ascending=False)

        # Plot win rates for all teams at the current venue
        sns.barplot(
            data=venue_data,
            x="Team",
            y="Win Rate",
            ax=axes[i],
            palette=team_color_dict,
        )
        axes[i].set_title(f"Win Rate at {venue}")
        axes[i].set_xlabel("")
        axes[i].set_ylabel("Win Rate")
        axes[i].set_ylim(0, 1)  # Set y-axis limit to ensure consistency

        # Rotate x-axis labels for better readability
        axes[i].tick_params(axis="x", rotation=90)

        # Hide x-axis tick labels
        axes[i].set_xticklabels([])

        # Hide y-axis label for all but the first column
        if i % num_cols != 0:
            axes[i].set_ylabel("")

        # Annotate highest win rate
        axes[i].annotate(
            "Highest",
            xy=(sorted_data.iloc[0]["Team"], sorted_data.iloc[0]["Win Rate"]),
            xytext=(-20, 5),
            textcoords="offset points",
            arrowprops=dict(facecolor="black", arrowstyle="->"),
        )

        # Annotate lowest win rate
        axes[i].annotate(
            "Lowest",
            xy=(
                sorted_data.iloc[-1]["Team"],
                sorted_data.iloc[-1]["Win Rate"],
            ),
            xytext=(-20, -15),
            textcoords="offset points",
            arrowprops=dict(facecolor="black", arrowstyle="->"),
        )

    sorted_teams = sorted(teams)
    legend_patches = [Patch(color=team_color_dict[team], label=team) for team in sorted_teams]
    fig.legend(handles=legend_patches, loc='upper right')
    # Adjust layout
    plt.tight_layout(pad=10)
    plt.show()


plot_winrates_by_venue(df)
