def organize_game_times(file):
    with open ("game_times_organized.txt", 'w') as output:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in range(0, len(lines) - 3):
                    if lines[line].startswith('[White "Urlsnylmz"]'):
                        output.write(lines[line])
                        output.write(lines[line + 1])
                        output.write(lines[line + 2])
                    elif lines[line].startswith('[Black "Urlsnylmz"]'):
                        output.write(lines[line - 1])
                        output.write(lines[line])
                        output.write(lines[line + 1])
                    elif lines[line].startswith("[UTCTime"):
                        output.write(lines[line])
                        output.write("\n")
                f.close()
                output.close()
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")

        
organize_game_times("games.pgn")
