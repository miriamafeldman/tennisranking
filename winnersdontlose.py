#Problem 3: Winners don't Lose

from matchresult import match_result

def wdl_score(data, players, year_start, year_end):
    """Arguments: data (dictionary), players (list), year_start (numeric), year_end (numeric)
    Returns: points (dictionary, with player as key and WdL score as value)
    Description: Calculates 'Winners Don't Lose' score for each player in time range specified
    """
    #Create empty dictionary for players range given
    players_all = []
    for i in range(year_start, year_end + 1):
        for player in players[i]:
            players_all.append(player)
    players_all = list(set(players_all))
    points = {player: 0 for player in players_all}

    #Fill with points
    for year in range(year_start, year_end + 1):
        for tournament in data[year]:
            for match in data[year][tournament]:
                winner, loser = match_result(match)
                rnd = match[11]
                points[winner] += rnd
                try:
                    points[loser] -= 1/rnd
                except:
                    points[loser] += 0
                    #print(f'{tournament}, {match[4]} vs {match[5]}, Zero!')
                    #There should never be a round zero so should try to elim this at some point
    
    return points

def wdl_rank(data, players, year_start, year_end):
    """Arguments: data (dictionary), players (list), year_start (numeric), year_end (numeric)
    Returns: list of lists, each with player as first element and WdL score as second element
    Sorted in descending order
    Description: Ranks players based on WdL algorithm in time range specified"""
    #Get points
    wdls = wdl_score(data, players, year_start, year_end)
    
    #Sort and rank
    rank_list = list(map(list, wdls.items()))
    rank_list.sort(key=lambda x:x[1], reverse = True)
    
    return rank_list   