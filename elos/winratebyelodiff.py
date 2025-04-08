import pandas as pd
import matplotlib.pyplot as plt


def elo_chart(file):
    # Create an empty DataFrame with the required columns
    game_data = pd.DataFrame(columns=["Opponent Elo", "My Elo", "Elo Difference", "Win-Lose-Tie"])

    try:
        with open(file, "r") as f:
            lines = f.readlines()
            my_username = "Urlsnylmz"
            current_game = {"Opponent Elo": None, "My Elo": None, "Elo Difference": None, "Win-Lose-Tie": None}

            for line in range(0, len(lines), 6):
                try:
                    # Parse game data
                    if lines[line].startswith(f'[White "{my_username}"]'):
                        result = lines[line + 2].split('"')[1]
                        current_game["Win-Lose-Tie"] = (
                            "Win" if result == "1-0" else "Lose" if result == "0-1" else "Tie"
                        )
                        current_game["My Elo"] = int(lines[line + 3].split('"')[1])
                        current_game["Opponent Elo"] = int(lines[line + 4].split('"')[1])
                    else:
                        result = lines[line + 2].split('"')[1]
                        current_game["Win-Lose-Tie"] = (
                            "Lose" if result == "1-0" else "Win" if result == "0-1" else "Tie"
                        )
                        current_game["My Elo"] = int(lines[line + 4].split('"')[1])
                        current_game["Opponent Elo"] = int(lines[line + 3].split('"')[1])

                    # Calculate Elo difference
                    current_game["Elo Difference"] = current_game["My Elo"] - current_game["Opponent Elo"]

                    # Append to DataFrame
                    game_data = pd.concat([game_data, pd.DataFrame([current_game])], ignore_index=True)

                except (IndexError, ValueError) as e:
                    print(f"Error parsing game data at line {line}: {e}")
                    continue  # Skip malformed game entries

                # Reset current_game for the next iteration
                current_game = {"Opponent Elo": None, "My Elo": None, "Elo Difference": None, "Win-Lose-Tie": None}

    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Add a Game No column for plotting
    game_data["Game No"] = range(1, len(game_data) + 1)

    # Segment the data
    segments = {
        "More than +150": game_data[game_data["Elo Difference"] >= 150],
        "+150 to +50": game_data[(game_data["Elo Difference"] >= 50) & (game_data["Elo Difference"] < 150)],
        "+50 to -50": game_data[(game_data["Elo Difference"] >= -50) & (game_data["Elo Difference"] < 50)],
        "-50 to -150": game_data[(game_data["Elo Difference"] >= -150) & (game_data["Elo Difference"] < -50)],
        "Less than -150": game_data[game_data["Elo Difference"] < -150],
    }

    # Calculate win rates
    def calculate_win_rate(segment):
        if len(segment) == 0:
            return 0  # Avoid division by zero
        wins = len(segment[segment["Win-Lose-Tie"] == "Win"])
        return wins / len(segment) * 100

    win_rates = {key: calculate_win_rate(segment) for key, segment in segments.items()}

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(win_rates.keys(), win_rates.values(), color="skyblue")
    plt.title("Win Rates by Elo Difference Segments")
    plt.xlabel("Elo Difference Segments")
    plt.ylabel("Win Rate (%)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Save the chart as an image
    plt.savefig("winrate_by_elo_difference.png")
    print("Bar chart saved as 'winrate_by_elo_difference.png'.")
    # Show the chart
    plt.show()
    
# Call the function with your file
elo_chart("elos_organised.txt")
