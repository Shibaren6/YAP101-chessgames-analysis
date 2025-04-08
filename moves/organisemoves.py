def organisemoves(file):
    with open ("moves_organised.txt", 'w') as output:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in range(0, len(lines)):
                    if lines[line].startswith('[White "Urlsnylmz"]'):
                        output.write(lines[line])
                    elif lines[line].startswith('[Black "Urlsnylmz"]'):
                        output.write(lines[line])
                    elif lines[line].startswith("1."):
                        output.write(lines[line])
                        output.write("\n")
                f.close()
                output.close()
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")

organisemoves("evalgames.pgn")