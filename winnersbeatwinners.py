#Problem 4 and Problem 5: WbW and Comparison

from matchresult import match_result
from datetime import datetime
from datetime import timedelta
import numpy as np
import sys

#Winners Beat Other Winners: Main Ranking Algorithm
def wbw_score(losses):
    """Calculates WbW algorithm scores over period
    Arguments: losses (dictionary), formatted according to wbw_years() or wbw_ytd()
        Key: player
        Values: loss total (in time range), list of opponents who defeated Key player
    Returns: scores (dictionary)
        Key: player
        Value: WbW score"""
    n = len(losses)
    scores = {player: 1/n for player in losses}

    #For convergence
    old_scores = {player: 0 for player in losses}

    #Iterate
    while not float_convergence(scores, old_scores):
        
        #Set old_scores
        old_scores = scores.copy()

        #Reset score updates
        score_updates = {player:0 for player in scores}

        #Fill score updates
        for player in scores: 
            loss_total = losses[player][0]
            opponents = losses[player][1]
            if loss_total == 0:
                score_updates[player] += scores[player]
            else:
                share_to_give = scores[player]/loss_total
                for opponent in opponents:
                    score_updates[opponent] += share_to_give
        
        #Update scores
        for player in scores: 
            scores[player] = (score_updates[player]*0.85)+(0.15/n)   

    return scores

def float_convergence(dict1, dict2):
    """Checks whether all values in two dictionaries with same keys and floats as values
    Have converged within +- system epsilon
    Arguments: dict1 (dictionary), dict2 (dictionary)
    Returns: result (Boolean)"""
    epsilon = sys.float_info.epsilon
    result = True
    for i in dict1:
        if not dict2[i] - epsilon <= dict1[i] <= dict2[i] + epsilon:
            result = False
    
    return result

#Annual
def wbw_years(data, players, year_start, year_end):
    """Calculates WbW score in time range specified
    Arguments: data (dictionary), players (list), year_start (numeric), year_end (numeric)
    Returns: dictionary with players as keys and WbW scores as values from wbw_score()"""
    #Create empty dictionary for players in range given
    players_all = list(set([player for i in range(year_start, year_end + 1)for player in players[i]]))
    losses = {i:[0, []] for i in players_all}

    #Fill  with losses and who defeated
    for year in range(year_start, year_end + 1):
        for tournament in data[year]:
            for match in data[year][tournament]:
                winner, loser = match_result(match)
                losses[loser][0] += 1
                losses[loser][1].append(winner) 
    
    return wbw_score(losses)

def wbw_rank(data, players, year_start, year_end):
    """Ranks players based on WbW algorithm in time range specified
    Arguments: data (dictionary), tournament (string), year (numeric)
    Returns: list of lists, each with player as first element and WbW score as second element
    Sorted in descending order"""
    #Get win totals
    wbw = wbw_years(data, players, year_start, year_end)

    #Sort and rank
    rank_list = list(map(list, wbw.items()))
    rank_list.sort(key=lambda x:x[1], reverse = True)

    return rank_list 

#Year to Date Functions
def wbw_ytd(data, year, tournament):
    """Calculates WbW score in 52 Weeks prior to tournament start
    Arguments: data (dictionary), players (list), tournament (string)
    Returns: dictionary with players as keys and WbW scores as values from wbw_score()"""

    #Get start date of tournament
    start_date = data[year][tournament][0][0]
    end_date = data[year][tournament][0][1]
    year_ago = start_date - timedelta(weeks = 52)

    #Initialise dictionary of tournaments in last year
    past_year = {year - 1: {}, year: {}}
    players_pastyr = []

    #Tournaments in prior year, completed within a year of tournament start_date
    for tournament in data[year - 1]:
        if data[year - 1][tournament][0][1] > year_ago:
            past_year[year - 1][tournament] = data[year - 1][tournament].copy()
            for match in data[year - 1][tournament]:
                players_pastyr.extend((match[3], match[4]))
    
    #Tournaments in year, completed prior to tournament end_date
    for tournament in data[year]:
        if data[year][tournament][0][1] < end_date:
            past_year[year][tournament] = data[year][tournament].copy()
            for match in data[year][tournament]:
                players_pastyr.extend((match[3], match[4]))

    players_pastyr = list(set(players_pastyr))

    #Losses
    losses = {i:[0, []] for i in players_pastyr}

    #Fill  with losses and who defeated
    for yr in range(year - 1, year + 1): 
        for tournament in past_year[yr]:
            for match in past_year[yr][tournament]:
                winner, loser = match_result(match)
                losses[loser][0] += 1
                losses[loser][1].append(winner)
    
    return wbw_score(losses)
    
def wta_rank(data, year, tournament):
    """Returns dictionary with player name as key and WTA Rank as value for players in tournament
    Based on WTA rank at start of tournament"""
    wta_dict = {}        
    
    for match in data[year][tournament]:
        if match[3] not in wta_dict:
            if match[5] != None:
                wta_dict[match[3]] = match[5]
            else:
                wta_dict[match[3]] = np.nan
        if match[4] not in wta_dict:
            if match[6] != None:
                wta_dict[match[4]] = match[6]
            else:
                wta_dict[match[4]] = np.nan

    return wta_dict

def wbw_wta_rank_ytd(data, year, tournament):
    """Ranks players based on WbW algorithm in 52 Weeks prior to tournament in year
    Arguments: data (dictionary), tournament (string), year (numeric)
    Returns: rank_dict (dictionary), each with player as key and list of WbW and WTA rankings as value
    Sorted in descending order"""
    #Get wbw
    wbw = wbw_ytd(data, year, tournament)

    #Sort and rank
    rank_list = list(map(list, wbw.items()))
    rank_list.sort(key=lambda x:x[1], reverse = True)
    
    #Dictionaries
    wbw_dict = {item[0]: rank_list.index(item) + 1 for item in rank_list}
    wta_dict = wta_rank(data, year, tournament)
    rank_dict = {p: [wbw_dict[p], wta_dict[p]] if p in wbw_dict.keys() else [np.nan, np.nan] for p in wta_dict}
    
    return rank_dict  

#Source: https://stackoverflow.com/questions/23190017/is-pythons-epsilon-value-correct?rq=1   