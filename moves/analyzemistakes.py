import csv
import matplotlib.pyplot as plt

# Define intervals for mistakes and blunders
def classify_move(eval_change, player_color):
    if player_color == "White":
        if -2.5 < eval_change <= -1.5:
            return "Mistake"
        elif eval_change <= -2.5:
            return "Blunder"
    elif player_color == "Black":
        if 1.5 < eval_change <= 2.5:
            return "Mistake"
        elif eval_change >= 2.5:
            return "Blunder"
    return "Other"

# Initialize counters
mistakes = 0
blunders = 0
total_moves = 0

# Read the chess_moves.csv file
file_path = r"c:\Users\Ural\OneDrive\Documents\GitHub\YAP101-chessgames-analysis\chess_moves.csv"

with open(file_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            eval_change = float(row["EvalChange"])
            player_color = row["PlayerColor"]
            total_moves += 1

            # Classify the move
            classification = classify_move(eval_change, player_color)
            if classification == "Mistake":
                mistakes += 1
            elif classification == "Blunder":
                blunders += 1
        except ValueError:
            # Skip rows with missing or invalid data
            continue

# Calculate other moves
other_moves = total_moves - (mistakes + blunders)

# Print results
print(f"Total Moves: {total_moves}")
print(f"Mistakes: {mistakes}")
print(f"Blunders: {blunders}")
print(f"Other Moves: {other_moves}")

# Create a pie chart
labels = ["Mistakes", "Blunders", "Other Moves"]
sizes = [mistakes, blunders, other_moves]
colors = ["orange", "red", "green"]
explode = (0.1, 0.1, 0)  # Highlight mistakes and blunders

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
plt.title("Analysis of Mistakes and Blunders in Chess Games")
plt.show()