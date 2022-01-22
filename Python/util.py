from genericpath import exists
import os
import urllib.request
import pandas as pd
import json
import statsmodels.formula.api as smf
import numpy as np

import constants as const

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def loadVaccines(path=f'data{os.sep}latest.csv'):
    fullDF = pd.read_csv(path)
    
    return fullDF

def preProcessing(neededDF):
    vaccinati = neededDF.drop(['area', 'sesso_maschile','sesso_femminile','prima_dose','pregressa_infezione','dose_addizionale_booster','codice_NUTS1','codice_NUTS2'], axis=1)
    vaccinati = vaccinati.loc[(vaccinati["seconda_dose"] > 0)].reset_index(drop=True)
    vaccinati['nome_area'].loc[(vaccinati["nome_area"] == 'Provincia Autonoma Trento')] = 'Provincia Autonoma Bolzano / Bozen'
    vaccinati.loc[(vaccinati["nome_area"] == 'Provincia Autonoma Bolzano / Bozen')]
    vaccinati['nome_area'].loc[(vaccinati["nome_area"] == 'Provincia Autonoma Bolzano / Bozen')] = 'Trentino Alto Adige'
    vaccinati.loc[(vaccinati["nome_area"] == 'Trentino Alto Adige')]

    return vaccinati

def getLatestVaccineReport(url=const.LATEST_REPORT_URL, dir='data', filename='latest.csv'):
    if not os.path.isdir(dir):
        print(f'[i] {dir} folder not found... creating it')
        os.mkdir(dir)
        os.chdir(dir)
        urllib.request.urlretrieve(url, dir)
        os.chdir("..")
        print('[i] ' + filename + ' downloaded in ' + dir + " folder")
    else:
        os.chdir(dir)
        urllib.request.urlretrieve(url, filename)
        os.chdir("..")
        print('[i] ' + filename + ' downloaded in existing folder: ' + dir)

    return True

def regTotalVaccines(region):
    fullDF = loadVaccines()
    df = preProcessing(neededDF=fullDF)
    if isinstance(region, int) is True:
        val = df.loc[df['codice_regione_ISTAT'] == region]['seconda_dose'].sum()
        reg = df.loc[df['codice_regione_ISTAT'] == region]['nome_area'].iloc[0]
    else:
        val = df.loc[df['nome_area'] == region]['seconda_dose'].sum()
        reg = region
    #print(f"La regione {reg} ha un totale di {val} vaccinati")
    return val

def SVI():
    """
    Function to load the stored value for Social Vulnerable Index and PIL of region
    """
    if os.path.isfile(f'data{os.sep}regionSVI_PIL.json') is True:
        exists = True
    else:
        exists = False


    if exists is False:
        dictFactors = {
        1: {'mono_Family': 6.8, 
                'six_more_Family': 0.8, 
                'low_Educ': 1.3,
                'ass_Unease': 3.2,
                'house_Crow': 1.1,
                'u30_Unemployed': 8.9,
                'eco_Unease': 1.4,
        'tot_Dosi': regTotalVaccines(1), 
                'residenti': 4274945,
        'PIL' : 126374.6},
        2: {'mono_Family': 7.2, 
                'six_more_Family': 0.7, 
                'low_Educ': 1.0,
                'ass_Unease': 2.8,
                'house_Crow': 1.2,
                'u30_Unemployed': 8.3,
                'eco_Unease': 1.0,
        'tot_Dosi': regTotalVaccines(2), 
                'residenti': 124089,
        'PIL' : 4522.4},
        3: {'mono_Family': 6.3, 
                'six_more_Family': 1.1, 
                'low_Educ': 1.4,
                'ass_Unease': 2.7,
                'house_Crow': 1.2,
                'u30_Unemployed': 8.1,
                'eco_Unease': 1.2,
        'tot_Dosi': regTotalVaccines(3), 
                'residenti': 9981554,
        'PIL' : 367167.2},
        4: {'mono_Family': 7.1, 
                'six_more_Family': 1.8, 
                'low_Educ': 0.8,
                'ass_Unease': 2.6,
                'house_Crow': 1.1,
                'u30_Unemployed': 6.7,
                'eco_Unease': 0.9,
        'tot_Dosi': regTotalVaccines(4), 
                'residenti': 1077078,
        'PIL' : 43821.9},
        5: {'mono_Family': 6.0, 
                'six_more_Family': 1.5, 
                'low_Educ': 1.1,
                'ass_Unease': 2.8,
                'house_Crow': 0.7,
                'u30_Unemployed': 7.4,
                'eco_Unease': 1.1,
        'tot_Dosi': regTotalVaccines(5), 
                'residenti': 4869830,
        'PIL' : 152340.6},
        6: {'mono_Family': 6.5, 
                'six_more_Family': 1.0, 
                'low_Educ': 0.7,
                'ass_Unease': 3.0,
                'house_Crow': 0.6,
                'u30_Unemployed': 7.5,
                'eco_Unease': 1.0,
        'tot_Dosi': regTotalVaccines(6), 
                'residenti': 1201510,
        'PIL' : 36814.3},
        7: {'mono_Family': 7.7, 
                'six_more_Family': 0.7, 
                'low_Educ': 1.3,
                'ass_Unease': 3.7,
                'house_Crow': 1.2,
                'u30_Unemployed': 9.2,
                'eco_Unease': 1.4,
        'tot_Dosi': regTotalVaccines(7), 
                'residenti': 1518495,
        'PIL' : 46194.7},
        8: {'mono_Family': 6.8, 
                'six_more_Family': 1.3, 
                'low_Educ': 1.4,
                'ass_Unease': 3.5,
                'house_Crow': 1.1,
                'u30_Unemployed': 8.3,
                'eco_Unease': 1.1,
        'tot_Dosi': regTotalVaccines(8), 
                'residenti': 4438937,
        'PIL' : 149633.0},
        9: {'mono_Family': 7.0, 
                'six_more_Family': 1.4, 
                'low_Educ': 1.2,
                'ass_Unease': 3.7,
                'house_Crow': 1.2,
                'u30_Unemployed': 9.2,
                'eco_Unease': 1.4,
        'tot_Dosi': regTotalVaccines(9), 
                'residenti': 3692865,
        'PIL' : 111605.6},
        10: {'mono_Family': 6.7, 
                'six_more_Family': 1.8, 
                'low_Educ': 1.1,
                'ass_Unease': 3.7,
                'house_Crow': 0.7,
                'u30_Unemployed': 8.9,
                'eco_Unease': 1.4,
            'tot_Dosi': regTotalVaccines(10), 
                'residenti': 865452,
        'PIL' : 21340.0},
        11: {'mono_Family': 6.5, 
                'six_more_Family': 1.8, 
                'low_Educ': 1.1,
                'ass_Unease': 3.9,
                'house_Crow': 1.0,
                'u30_Unemployed': 8.1,
                'eco_Unease': 1.3,
            'tot_Dosi': regTotalVaccines(11), 
                'residenti': 1498236,
        'PIL' : 39412.4},
        12: {'mono_Family': 9.1,
                'six_more_Family': 1.2, 
                'low_Educ': 1.0,
                'ass_Unease': 2.6,
                'house_Crow': 1.6,
                'u30_Unemployed': 11.9,
                'eco_Unease': 2.5,
            'tot_Dosi': regTotalVaccines(12), 
                'residenti': 5730399,
        'PIL' : 186306.9},
        13: {'mono_Family': 6.8, 
                'six_more_Family': 1.6, 
                'low_Educ': 1.2,
                'ass_Unease': 3.6,
                'house_Crow': 0.9,
                'u30_Unemployed': 10.3,
                'eco_Unease': 2.0,
            'tot_Dosi': regTotalVaccines(13), 
                'residenti': 1281012,
        'PIL' : 30662.3},
        14: {'mono_Family': 6.8, 
                'six_more_Family': 1.2, 
                'low_Educ': 1.3,
                'ass_Unease': 3.8,
                'house_Crow': 1.0,
                'u30_Unemployed': 11.5,
                'eco_Unease': 2.5,
            'tot_Dosi': regTotalVaccines(14), 
                'residenti': 294294,
        'PIL' : 6008.3},
        15: {'mono_Family': 8.0, 
                'six_more_Family': 2.8, 
                'low_Educ': 2.9,
                'ass_Unease': 2.2,
                'house_Crow': 3.5,
                'u30_Unemployed': 20.4,
                'eco_Unease': 7.6,
            'tot_Dosi': regTotalVaccines(15), 
                'residenti': 5624260,
        'PIL' : 102702.3},
        16: {'mono_Family': 6.1, 
                'six_more_Family': 1.5, 
                'low_Educ': 2.5,
                'ass_Unease': 3.1,
                'house_Crow': 1.6,
                'u30_Unemployed': 15.6,
                'eco_Unease': 4.3,
            'tot_Dosi': regTotalVaccines(16), 
                'residenti': 3933777,
        'PIL' : 70433.2},
        17: {'mono_Family': 5.5, 
                'six_more_Family': 1.1, 
                'low_Educ': 1.6,
                'ass_Unease': 3.6,
                'house_Crow': 1.4,
                'u30_Unemployed': 12.0,
                'eco_Unease': 3.1,
            'tot_Dosi': regTotalVaccines(17), 
                'residenti': 545130,
        'PIL' : 11480.3},
        18: {'mono_Family': 6.5, 
                'six_more_Family': 1.6, 
                'low_Educ': 3.0,
                'ass_Unease': 3.0,
                'house_Crow': 1.5,
                'u30_Unemployed': 17.6,
                'eco_Unease': 5.1,
            'tot_Dosi': regTotalVaccines(18), 
                'residenti': 1860601,
        'PIL' : 30759.1},
        19: {'mono_Family': 6.4, 
                'six_more_Family': 1.5, 
                'low_Educ': 3.1,
                'ass_Unease': 3.1,
                'house_Crow': 2.1,
                'u30_Unemployed': 19.4,
                'eco_Unease': 5.9,
                'tot_Dosi': regTotalVaccines(19), 
                'residenti': 4833705,
        'PIL' : 83065.0},
        20: {'mono_Family': 6.8, 
                'six_more_Family': 1.2, 
                'low_Educ': 1.5,
                'ass_Unease': 2.6,
                'house_Crow': 0.9,
                'u30_Unemployed': 12.2,
                'eco_Unease': 3.3,
                'tot_Dosi': regTotalVaccines(20), 
                'residenti': 1590044,
        'PIL' : 32121.0}}
        with open(f'data{os.sep}regionSVI_PIL.json', 'w') as json_file:
            json.dump(dictFactors, json_file, cls=NpEncoder, indent=4)

    newDF = pd.read_json(f'data{os.sep}regionSVI_PIL.json')

    return newDF
