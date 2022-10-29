def match_result(match):
    """Arguments: match (list)
    Returns: winner (string), loser (string)
    Description: Takes individual match data formatted by tennisdata.store_data() and returns name of winner and loser in order
    In cases where a player retires, the player who Retired is returned as loser"""

    #Incomplete Matches
    if match[10] != 'Completed':
        note_split = match[10].split(' Retired')
        loser_name = note_split[0]
        if match[3] == loser_name:
            winner = match[4]
            loser = match[3]
        else:
            winner = match[3]
            loser = match[4] 
        
        return winner, loser       
    
    #Complete Matches
    p1_wins = 0
    for j in range(7,10):
        if match[j] != '':
            p1s, p2s = match[j].split('-')
            if int(p1s) > int(p2s):
                p1_wins += 1
    
    #Winner assigned to player who wins best of match[2] 
    if p1_wins >= match[2]/2:
        winner = match[3]
        loser = match[4]
    else:
        winner = match[4]
        loser = match[3]

    return winner, loser
