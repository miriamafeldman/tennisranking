#Problem 2: Winners Win

from matchresult import match_result

def win_totals(data, players, year_start, year_end):
    """Arguments: data (dictionary), players (list), year_start (numeric), year_end (numeric)
    Returns: wins (dictionary, players as keys and win totals in period specified as values)
    Description: Counts number of wins per player in time range specified"""

    #Create empty dictionary for players range given
    players_all = [player for i in range(year_start, year_end + 1)for player in players[i]]
    players_all = list(set(players_all))
    wins = {i:0 for i in players_all}

    #Fill Dictionary
    for j in range(year_start, year_end + 1):
        for tournament in data[j]:
            for match in data[j][tournament]:
                winner, loser = match_result(match)
                wins[winner] += 1    
    return wins

def wins_ranking(data, players, year_start, year_end):
    """Arguments: data (dictionary), players (list), year_start (numeric), year_end (numeric)
    Returns: rank_list (list of lists, each [Player, Win Total], sorted in decreasing order by win total)
    Description: Ranks players based on 'Winners Win' algorithm in time range specified"""
    
    #Get win totals
    wins = win_totals(data, players, year_start, year_end)

    #Sort and rank
    rank_list = list(map(list, wins.items()))
    rank_list.sort(key=lambda x:x[1], reverse = True)

    return rank_list

#Sources
#Dictionary to list: https://stackoverflow.com/questions/7436267/python-transform-a-dictionary-into-a-list-of-lists/37852096 Gurucharan M K
#Sort by second element: https://www.pythonpool.com/python-sort-list-of-lists/