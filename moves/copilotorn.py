import re
import pandas as pd

# Load the file content
file_path = "moves_organised.txt"  # Replace with the actual file path
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Split the content into individual games
games = re.split(r'\[White "Urlsnylmz"\]', content)
games = [game.strip() for game in games if game.strip()]  # Remove empty entries

# Initialize a list to store parsed data
data = []

# Process each game
for game_index, game in enumerate(games, start=1):
    # Determine the player color
    player_color = "White" if "Urlsnylmz" in game.splitlines()[0] else "Black"
    
    # Extract moves, time remaining, and evaluations using regex
    moves = re.findall(r'(\d+\.\s*[^{}]+)\s*{[^}]*\[%eval\s*([#\d\.\-]+)\]\s*\[%clk\s*([\d:]+)\]', game)
    
    previous_eval = None  # To calculate evaluation change
    
    for move_number, (move, eval_after, time_remaining) in enumerate(moves, start=1):
        # Split the move into white's and black's moves (if both exist)
        white_move, black_move = (move.split(" ") + [None])[:2]
        
        # Determine the current move and player
        if player_color == "White":
            current_move = white_move
            is_my_move = move_number % 2 == 1  # White moves on odd numbers
        else:
            current_move = black_move
            is_my_move = move_number % 2 == 0  # Black moves on even numbers
        
        # If it's your move, process the data
        if is_my_move and current_move:
            # Convert evaluation to a numeric value (handle mate evaluations)
            if eval_after.startswith("#"):
                eval_numeric = float('inf') if eval_after[1] == "+" else float('-inf')
            else:
                eval_numeric = float(eval_after)
            
            # Calculate evaluation change
            eval_change = None
            if previous_eval is not None:
                eval_change = eval_numeric - previous_eval
            
            # Append the data
            data.append({
                "Game": game_index,
                "MoveNumber": move_number,
                "Move": current_move,
                "TimeRemaining": time_remaining,
                "EvalAfter": eval_numeric,
                "EvalChange": eval_change,
                "PlayerColor": player_color  # Add player color
            })
            
            # Update the previous evaluation
            previous_eval = eval_numeric
    
    # Add a blank row to separate games
    data.append({
        "Game": None,
        "MoveNumber": None,
        "Move": None,
        "TimeRemaining": None,
        "EvalAfter": None,
        "EvalChange": None,
        "PlayerColor": None
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the DataFrame
print(df.head())

# Save to a CSV file
df.to_csv("chess_moves.csv", index=False, lineterminator="\n")  # Ensure newline at the end