#Problem 1: Reconstructing Tournaments

from matchresult import match_result
from math import log
from math import ceil
from statistics import mean

def get_rounds(data, year, tournament):
    """Arguments: data (dictionary), year (numeric), tournament (string)
    Returns: N/A
    Description: Modifies dictionary in place, appending round numbers and names (e.g. 'Semifinal', 'Final') to matches
    Assumes data is stored and formatted as output of tennisdata.storedata()"""
    
    #Player Stats
    stats = {}
    for match in data[year][tournament]:
        #Get Players and Ranks
        p1, p2 = match[3:5]
        
        try:
            r1 = int(match[5])
        except:
            r1 = 0
        try:
            r2 = int(match[6])
        except:
            r2 = 0
    
        
        #Add Number of Matches Played, Losses
        try:
            stats[p1]['P'] += 1
        except:
            stats[p1] = {'Rank': r1, 'P':0, 'L': 0, 'P (Adjusted)':0}
            stats[p1]['P'] += 1
        try:
            stats[p2]['P'] += 1
        except:
            stats[p2] = {'Rank': r2, 'P':0, 'L': 0, 'P (Adjusted)':0}
            stats[p2]['P'] += 1

        winner, loser = match_result(match)
        stats[loser]['L'] += 1
    

    #Functions for appending round names by tournament type
    #Tournament types: Knockout, Round Robin
    def round_names_knockout(p1, p2, rnds):
        """Arguments: p1 (string), p2 (string), rnds (numeric, rounds in tournament)
        Returns: N/A
        Description: Appends name of rounds 'Semifinal', 'Third Place' and 'Final' to match data in place"""
        for match in data[year][tournament]:
            if match[11] == rnds:
                if stats[p1]['L'] == 0 or stats[p2]['L'] == 0:
                    match.append('Final')
                else:
                    match.append('Third Place')
            elif match[11] == rnds - 1:
                match.append('Semifinal')
            else:
                match.append(match[11])
    
    def round_names_rr(p1, p2, rnds):
        """Arguments: p1 (string), p2 (string), rnds (numeric, rounds in tournament)
        Returns: N/A
        Description: Appends name of rounds 'RR', 'Semifinal', and 'Final' to match data in place"""
        #Round Robin
        for match in data[year][tournament]:
            if match[11] == 1:
                match.append('RR')
            elif match[11] == rnds:
                match.append('Final')
            elif match[11] == rnds - 1:
                match.append('Semifinal')
            else:
                match.append(match[11])


    #Functions for determining round numbers
    #Tournament types: Knockout (no byes), Knockout (with byes), Round Robin
    def knockout_nobyes():
        """Arguments: N/A
        Returns: N/A
        Description: Appends round numbers to matches in place"""
        rnd_list = []

        #Append round numbers to matches
        for match in data[year][tournament]:
            p1, p2 = match[3:5]
            rnd = min(stats[p1]['P'], stats[p2]['P'])
            rnd_list.append(rnd)
            match.append(rnd)
        
        #Get number of rounds in tournament
        rnds = max(rnd_list)

        #Append round names to matches
        round_names_knockout(p1, p2, rnds)
    
    def knockout_byes(byes):
        """Arguments: byes (numeric type, number of players granted byes in tournament)
        Returns: N/A
        Description: Appends round numbers to matches in place"""
        rnd_list = []

        #Assumes "Byes will be given to seeded players in descending order" (Source: 3)
        sorted_ranks = sorted([stats[player]['Rank'] for player in stats])
        top_ranks = sorted_ranks[:byes]

        #Assign P (Adjusted) based on rank
        for player in stats:
            if stats[player]['Rank'] in top_ranks:
                stats[player]['P (Adjusted)'] += stats[player]['P'] + 1
            else:
                stats[player]['P (Adjusted)'] += stats[player]['P']

        #Append round numbers to matches
        for match in data[year][tournament]:
            p1, p2 = match[3:5]
            rnd = min(stats[p1]['P (Adjusted)'], stats[p2]['P (Adjusted)'])
            rnd_list.append(rnd)
            match.append(rnd)
    
        #Get number of rounds in tournament
        rnds = max(rnd_list)

        #Append round names to matches
        round_names_knockout(p1, p2, rnds)
        
    def round_robin():
        """Arguments: N/A
        Returns: N/A
        Description: Appends round numbers to matches in place, with matches in Round Robin stage assigned Round 1
        Assumes no more than half of the players survive the Round Robin Stage"""
        rnd_list = []
        
        #Determine players eliminated in Round Robin vs Knockout stage
        avg_played = mean([stats[player]['P'] for player in stats])
        ko = [player for player in stats if stats[player]['P'] > avg_played]
        rr_elim = [player for player in stats if player not in ko]
        
        #Determine Round Robin and Knockout stage lengths
        rr_matches_pp = max([stats[player]['P'] for player in rr_elim])
        ko_matches = len(ko) - 1
        
        #Append round numbers to matches
        for match in data[year][tournament]:
            p1, p2 = match[3:5]
            
            #ASSUMPTION: Rely on order of matches in tournament data if two players who survive Round Robin play during Round Robin
            if p1 in rr_elim or p2 in rr_elim:
                rnd = 1
            else:
                match_index = data[year][tournament].index(match)
                if match_index < len(data[year][tournament]) - ko_matches:
                    rnd = 1
                else:
                    rnd = min(stats[p1]['P'] - rr_matches_pp + 1, stats[p2]['P'] - rr_matches_pp + 1)

            match.append(rnd)
            rnd_list.append(rnd)
        
        #Get number of rounds in tournament
        rnds = max(rnd_list)
        
        #Append round names to matches
        round_names_rr(p1, p2, rnds)

    #Determining Tournament Type
    #Tournament types: Knockout (no byes), Knockout (with byes), Round Robin
    #A. Round Robin Checkpoint
    multi_loss = 0
    for player in stats:
        if stats[player]['L'] >= 2:
            multi_loss += 1
    
    if multi_loss >= 2:
        round_robin()

    else:
        #B. Byes Checkpoint (Source: 1, 2)
        num_players = len(stats)
        pow_2 = pow(2, ceil(log(num_players)/log(2)))
        byes = pow_2 - num_players
        if byes == 0:
            knockout_nobyes()
        else:
            knockout_byes(byes)


#Sources:
#1: https://stackoverflow.com/questions/466204/rounding-up-to-next-power-of-2 User: Paul Dixon
#2: https://www.printyourbrackets.com/how-byes-work-in-a-tournament.html
#3: https://photoresources.wtatennis.com/wta/document/2021/03/08/d6d2c650-e3b4-42e7-ab2b-e539d4586033/2021Rulebook.pdf Section V.A.1.a.v




#Mini Functions for Questions
def tourn_winner(data, year, tournament):
    """Arguments: data (dictionary), year (numeric), tournament (string)
    Returns: winner (string)
    Description: Finds winner of given tournament in year specified"""
    for match in data[year][tournament]:
        if match[12] == 'Final':
            winner = match_result(match)[0]
    
    return winner

def round_matchups(data, year, tournament, rnd):
    """Arguments: data (dictionary), year (numeric), tournament (string), rnd (numeric)
    Returns: matchups (list)
    Description: Finds matchups ('Player 1 vs Player 2') in round provided of tournament in year specified"""
    matchups = []
    for match in data[year][tournament]:
        if match[11] == rnd:
            matchups.append(f'{match[3]} vs {match[4]}')
    
    return matchups

def round_elim(data, year, tournament, player):
    """Arguments: data (dictionary), year (numeric), tournament (string), player (string)
    Returns: round number (numeric)
    Description: Finds which round player was eliminated from tournament in year specified"""
    rnd_elim = 1
    for match in data[year][tournament]:
        if match_result(match)[1] == player:
            rnd_elim = match[11]
            #Continues through Round Robin stage losses
            if match[12] == 'RR':
                continue
            else:
                break
    
    return rnd_elim  

def player_finals(data, player):
    """Arguments: data (dictionary), player (string)
    Returns: finals (numeric)
    Description: Counts how many finals player has appeared in across all years in data set"""
    finals = 0
    for year in data:
        for tournament in data[year]:
            for match in data[year][tournament]:
                if match[12] == 'Final' and (match[3] == player or match[4] == player):
                    finals +=1
    
    return finals

def headtohead(data, p1, p2):
    """Arguments: data (dictionary), p1 (string), p2 (string)
    Returns: matches (numeric), wins (dictionary, with p1 and p2 as keys and win counts as values)
    Description: For two given players, counts how many matches they have played in against one another
    And how many of these each has won"""
    players = [p1, p2]
    wins = {player: 0 for player in players}
    matches = 0
    for year in data:
        for tournament in data[year]:
            for match in data[year][tournament]:
                mp1 = match[3]
                mp2 = match[4]
                if [mp1, mp2] == players or [mp2, mp1] == players:
                    matches += 1
                    winner, loser = match_result(match)
                    wins[winner] += 1
    
    return matches, wins