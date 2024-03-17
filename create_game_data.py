import pandas as pd
import json
import os
import argparse


def load_and_save_data(data_file, save_dir):
    # Load data from JSON file
    with open(data_file, "r") as fn:
        data = json.load(fn)

    # Empty DataFrame to store rearranged data
    df = pd.DataFrame()

    # Loop through data to extract relevant information
    for entry in data:
        year = entry["year"]
        for round_number, games in entry["rounds"].items():
            for game in games:
                teams = game["teams"]
                game_data = {
                    "Year": year,
                    "Round": round_number,
                    "Date": game["date"],
                    "Venue": game["venue"],
                    "Attendance": game["attendance"],
                    "Outcome": game["outcome"],
                    "Margin": game["margin"],
                }

                for i, team in enumerate(teams):
                    game_data[f"Team{i+1}"] = team["name"]
                    game_data[f"Team{i+1} Score"] = team["final_score"]
                    if not game_data.get("Winner"):
                        game_data["Winner"] = team["name"] if team["won"] else None

                        # not using quarter scores currently
                        # for quarter, scores in team["quarter_scores"].items():
                        #     team_data[f"Quarter {quarter} Goals"] = scores["goals"]
                        #     team_data[f"Quarter {quarter} Conversions"] = scores["conversions"]

                df = df.concat({**game_data}, ignore_index=True)

    # Reordering columns for better readability
    columns = [
        "Year",
        "Round",
        "Date",
        "Venue",
        "Team1",
        "Team2",
        "Winner"
        "Attendance",
        "Outcome",
        "Margin",
        "Team1 Score",
        "Team2 Score",
        
    ]#Year,Round,Date,Venue,Attendance,Outcome,Margin,Team1,Team1 Score,Winner,Team2,Team2 Score
    # for quarter in range(1, 5):
    #     columns.extend([f"Quarter {quarter} Goals", f"Quarter {quarter} Conversions"])

    df = df.reindex(columns=columns)

    # Save DataFrame as CSV file
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    csv_filename = os.path.join(save_dir, "football_data.csv")
    df.to_csv(csv_filename, index=False)
    print(f"Data saved successfully to: {csv_filename}")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Load and rearrange AFL data from JSON file and save as CSV"
    )
    parser.add_argument("data_file", type=str, help="Path to the JSON data file")
    parser.add_argument(
        "--save_dir",
        type=str,
        default="data",
        help='Directory to save the CSV file (default: "data")',
    )
    args = parser.parse_args()

    # Load and save data
    load_and_save_data(args.data_file, args.save_dir)


if __name__ == "__main__":
    # main()
    load_and_save_data("2018_2022_data.json", "data")
