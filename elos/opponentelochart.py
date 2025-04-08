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
                    if lines[line].startswith(f'[White "{my_username}"]'):
                        result = lines[line + 2].split('"')[1]
                        my_elo = lines[line + 3].split('"')[1]
                        opponent_elo = lines[line + 4].split('"')[1]

                        # Handle unknown Elo ratings (?)
                        if my_elo == "?" or opponent_elo == "?":
                            continue  # Skip games with unknown Elo ratings

                        current_game["Win-Lose-Tie"] = (
                            "Lose" if result == "0-1" else "Win" if result == "1-0" else "Tie"
                        )
                        current_game["My Elo"] = int(my_elo)
                        current_game["Opponent Elo"] = int(opponent_elo)
                        current_game["Elo Difference"] = current_game["My Elo"] - current_game["Opponent Elo"]
                        game_data = pd.concat([game_data, pd.DataFrame([current_game])], ignore_index=True)
                    else:
                        result = lines[line + 2].split('"')[1]
                        my_elo = lines[line + 4].split('"')[1]
                        opponent_elo = lines[line + 3].split('"')[1]

                        # Handle unknown Elo ratings (?)
                        if my_elo == "?" or opponent_elo == "?":
                            continue  # Skip games with unknown Elo ratings

                        current_game["Win-Lose-Tie"] = (
                            "Win" if result == "0-1" else "Lose" if result == "1-0" else "Tie"
                        )
                        current_game["My Elo"] = int(my_elo)
                        current_game["Opponent Elo"] = int(opponent_elo)
                        current_game["Elo Difference"] = current_game["My Elo"] - current_game["Opponent Elo"]
                        game_data = pd.concat([game_data, pd.DataFrame([current_game])], ignore_index=True)

                    current_game = {"Opponent Elo": None, "My Elo": None, "Elo Difference": None, "Win-Lose-Tie": None}
                except ValueError:
                    print(f"Skipping invalid Elo data at line {line}.")

    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")

    # Add a Game No column for plotting
    game_data["Game No"] = range(1, len(game_data) + 1)
    print(game_data)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(game_data["Game No"], game_data["Opponent Elo"], label="Opponent Elo", marker="o")
    plt.plot(game_data["Game No"], game_data["My Elo"], label="My Elo", marker="x")
    plt.title("Elo Ratings Over Games")
    plt.xlabel("Game No")
    plt.ylabel("Elo")
    plt.legend()
    plt.grid(True)
    plt.show()


# Call the function with the file path
elo_chart("elos_organised.txt")
