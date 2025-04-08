def orgelos(file):
    with open ("elos_organised.txt", 'w') as output:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in range(len(lines) - 3):
                    if(lines[line].startswith('[White "Urlsnylmz"]')):
                        output.write(lines[line])
                        output.write(lines[line + 1])
                    elif(lines[line].startswith('[Black "Urlsnylmz"]')):
                        output.write(lines[line - 1])
                        output.write(lines[line])                        
                    elif(lines[line].startswith("[Result")):
                        output.write(lines[line])
                    elif(lines[line].startswith("[WhiteElo")):
                        output.write(lines[line])
                    elif(lines[line].startswith("[BlackElo")):
                        output.write(lines[line])
                        output.write("\n")
            f.close()
            output.close()
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        

orgelos("games.pgn")