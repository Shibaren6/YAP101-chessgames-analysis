import pandas as pd
import matplotlib.pyplot as plt

def calculate_winrate_by_time_of_day(file):
    game_data = pd.DataFrame(columns=["Time of Day", "Win-Lose-Tie"])
    try:
        with open(file, 'r') as f:
            current_game = {"Time of Day": None, "Win-Lose-Tie": None}
            lines = f.readlines()
            for line in range(0, len(lines), 5):
                if(lines[line].startswith('[White "Urlsnylmz"]')):
                    if(lines[line + 2].split('"')[1] == "0-1"):
                        current_game["Win-Lose-Tie"] = "Lose"
                    elif(lines[line + 2].split('"')[1] == "1-0"):
                        current_game["Win-Lose-Tie"] = "Win"
                    elif(lines[line + 2].split('"')[1] == "1/2-1/2"):
                        current_game["Win-Lose-Tie"] = "Tie"
                    
                else:
                    if(lines[line + 2].split('"')[1] == "0-1"):
                        current_game["Win-Lose-Tie"] = "Win"
                    elif(lines[line + 2].split('"')[1] == "1-0"):
                        current_game["Win-Lose-Tie"] = "Lose"
                    elif(lines[line + 2].split('"')[1] == "1/2-1/2"):
                        current_game["Win-Lose-Tie"] = "Tie"

                current_game["Time of Day"] = lines[line + 3].split('"')[1]
                game_data = pd.concat([game_data, pd.DataFrame([current_game])], ignore_index=True)
                current_game = {"Time of Day": None, "Win-Lose-Tie": None}

    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
        return

    game_data["Game No"] = range(1, len(game_data) + 1)

    # Filter games by time of day
    night_games = game_data[(game_data["Time of Day"] >= "22:00") | (game_data["Time of Day"] < "06:00")]
    afternoon_games = game_data[(game_data["Time of Day"] >= "17:00") & (game_data["Time of Day"] < "22:00")]
    morning_games = game_data[(game_data["Time of Day"] >= "06:00") & (game_data["Time of Day"] < "17:00")]

    # Calculate win rates
    def calculate_winrate(games):
        if len(games) == 0:
            return 0
        return len(games[games["Win-Lose-Tie"] == "Win"]) / len(games) * 100

    night_winrate = calculate_winrate(night_games)
    afternoon_winrate = calculate_winrate(afternoon_games)
    morning_winrate = calculate_winrate(morning_games)

    # Create bar graph
    time_periods = ['Night (22:00-06:00)', 'Afternoon (17:00-22:00)', 'Morning (06:00-17:00)']
    win_rates = [night_winrate, afternoon_winrate, morning_winrate]

    plt.bar(time_periods, win_rates, color=['blue', 'orange', 'green'])
    plt.xlabel('Time of Day')
    plt.ylabel('Win Rate (%)')
    plt.title('Win Rate by Time of Day')
    plt.ylim(0, 100)
    plt.show()

# Call the function with the file path
calculate_winrate_by_time_of_day("game_times_organized.txt")
