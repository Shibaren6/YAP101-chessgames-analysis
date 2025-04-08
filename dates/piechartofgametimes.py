import pandas as pd
import matplotlib.pyplot as plt

def create_piechart_of_gametimes(file):
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

    game_data["Game No"] = range(1, len(game_data) + 1)
    night_len = len(game_data[(game_data["Time of Day"] >= "22:00") | (game_data["Time of Day"] < "06:00")])
    afternoon_len = len(game_data[(game_data["Time of Day"] >= "17:00") & (game_data["Time of Day"] < "22:00")])
    morning_len = len(game_data[(game_data["Time of Day"] >= "06:00") & (game_data["Time of Day"] < "17:00")])

    print("total: " , len(game_data))
    print("night: ", night_len)
    print("afternoon: ", afternoon_len)
    print("morning: ", morning_len)

    # Create a pie chart
    labels = ['Night (22:00-06:00)', 'Afternoon (17:00-22:00)', 'Morning (06:00-17:00)']
    sizes = [night_len, afternoon_len, morning_len]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Optional: Custom colors
    explode = (0.1, 0, 0)  # Optional: Highlight the first slice (night games)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode)
    plt.title('Distribution of Chess Games by Time of Day')
    plt.show()

create_piechart_of_gametimes("game_times_organized.txt")