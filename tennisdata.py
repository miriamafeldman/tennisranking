#Data prep for Q1-Q5

import os
import csv
import numpy as np
from datetime import datetime

def get_paths(start, years):
    """Arguments: start (numeric), years (numeric, number of years/csv files)
    Returns: file_paths (list of local file paths for all years)
    Assumes file naming convention YYYY.csv"""
    #Get file paths for all tournament data files
    file_yrs = [start + i for i in range(years)]
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_paths = []

    for i in range(years): 
        file_path = os.path.join(file_dir, f'../assignment-final-data/{file_yrs[i]}.csv')
        file_paths.append(file_path)

    return file_paths

#Source: https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python User: Fahad Haleem


def get_data(fname):
    """Arguments: fname (string, file path to data file)
    Returns: data (dictionary), players (list)
    Description: Opens csv data file for WTA year. Returns a dictionary of formatted tournament match data and a list of players."""
    
    with open(fname, 'r') as f:
        csvreader = csv.reader(f)

        header = next(csvreader)
        
        data = {}
        players_full = []
        for row in csvreader:
            tourn, ds, de, bestof, p1, p2, r1, r2, s1, s2, s3, comment = row
            #Unranked players
            try:
                r1 = float(r1)
            except:
                r1 = None
            try: 
                r2 = float(r2)
            except:
                r2 = None            
            
            #If-else for tournaments across year end
            if de[-5:] == "12-31":
                try:
                    data[f'{tourn} 2'].append([datetime.strptime(ds, "%Y-%m-%d"), datetime.strptime(de, "%Y-%m-%d"), int(bestof), p1.strip(), p2.strip(), r1, r2, s1, s2, s3, comment])
                except:
                    data[f'{tourn} 2'] = []
                    data[f'{tourn} 2'].append([datetime.strptime(ds, "%Y-%m-%d"), datetime.strptime(de, "%Y-%m-%d"), int(bestof), p1.strip(), p2.strip(), r1, r2, s1, s2, s3, comment])
            else:
                try:
                    data[tourn].append([datetime.strptime(ds, "%Y-%m-%d"), datetime.strptime(de, "%Y-%m-%d"), int(bestof), p1.strip(), p2.strip(), r1, r2, s1, s2, s3, comment])
                except:
                    data[tourn] = []
                    data[tourn].append([datetime.strptime(ds, "%Y-%m-%d"), datetime.strptime(de, "%Y-%m-%d"), int(bestof), p1.strip(), p2.strip(), r1, r2, s1, s2, s3, comment])
            players_full.extend((p1, p2))
        
        players = list(set(players_full))
        
    f.close()
    return data, players


def store_data(start, years):
    """Arguments: start (numeric, first year) and years (numeric, number of years)
    Returns: data (dictionary with years as keys, csv tournament match data as values), 
    players (dictionary with years as keys, list of players as values)"""

    #Get names of file paths
    file_paths = get_paths(start, years)

    #Make empty dictionary to store data, key is tournament year
    data = {start + i:{} for i in range(years)}
    players = {start + i:[] for i in range(years)}

    #Load data into dictionary
    for i in range(years):
        data[start + i], players[start + i] = get_data(file_paths[i])


    return data, players


def fix_year_ends(data):
    """Arguments: data (dictionary) formatted according to store_data() function
    Returns: data (dictionary)
    Description: Returns data dictionary with restored tournaments (i.e. those which were split across year ends)
    Restored tournament is placed in year tournament was completed"""
    data_fye = data.copy()
    for year in data_fye:
        for tournament in data_fye[year]:
            end_date = data_fye[year][tournament][0][1]
            if end_date == datetime(year, 12, 31, 0, 0):
                #Find tournament name
                base_name = tournament[:-2]
                
                #Recreate
                first_half = data_fye[year][tournament].copy()
                second_half = data_fye[year + 1][base_name].copy()
                data_fye[year + 1][base_name] = first_half + second_half
    
    return data_fye