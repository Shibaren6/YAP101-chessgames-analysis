def extract_win_data(file):
    win = 0
    lose = 0
    tie = 0
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(0,len(lines) - 3):
            current_line = lines[i]
            preceeding_line = lines[i + 1]
            second_preceeding_line = lines[i + 2]
            if(current_line == '[White "Urlsnylmz"]\n'):
                if(second_preceeding_line == '[Result "0-1"]\n'):
                    lose = lose + 1
                elif(second_preceeding_line == '[Result "1-0"]\n'):
                    win = win + 1
                elif(second_preceeding_line == '[Result "1/2-1/2"]\n'):
                    tie = tie + 1
            elif(current_line == '[Black "Urlsnylmz"]\n'):
                if(preceeding_line == '[Result "0-1"]\n'):
                    win = win + 1
                elif(preceeding_line == '[Result "1-0"]\n'):
                    lose = lose + 1
                elif(preceeding_line == '[Result "1/2-1/2"]\n'):
                    tie = tie + 1
            f.close()
    total = win + lose + tie
    print("total games: ", total)
    print("wins: ", win)
    print("loses: ", lose)
    print("ties: ", tie)
    print("win percentage: ", win / total * 100)


extract_win_data("games.pgn")



