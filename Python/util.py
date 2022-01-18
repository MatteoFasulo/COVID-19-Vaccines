import os
import urllib.request
import pandas as pd

import constants as const

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

"""def preProcessing(csvFile: str = 'data/latest.csv'):
    assert(getLatestVaccineReport())
    df = pd.read_csv(csvFile)
    secondaDose = df.loc[(df["seconda_dose"] > 0)]
    return secondaDose

def regionVax(dataframe, result: bool = True):
    totPopolazioneItaliana = const.POP_ITA
    totUnder12 = const.POP_ITA_U12
    totOver12 = totPopolazioneItaliana - totUnder12

    if result is True:
        percentages = dataframe.groupby(['nome_area'])['seconda_dose'].apply(lambda x: (sum(x)/totPopolazioneItaliana)*100)
        return percentages

def fetchIVSM(fileName: str = "data/2011.xlsx", header=None):
    IVSM = pd.read_excel(fileName,header=header)
    trentino = IVSM.loc[IVSM[5]=='Trentino-Alto Adige/Südtirol']
    IVSM = pd.concat([IVSM,trentino],ignore_index=True)
    bolzanoIDX = IVSM.loc[IVSM[5]=='Trentino-Alto Adige/Südtirol'].index.tolist()[0]
    trentoIDX = IVSM.loc[IVSM[5]=='Trentino-Alto Adige/Südtirol'].index.tolist()[1]
    IVSM[5][bolzanoIDX] = 'Provincia Autonoma Trento'
    IVSM[5][trentoIDX] = 'Provincia Autonoma Bolzano'
    ivsmList = IVSM.groupby([5])[96].sum().tolist()
    return(ivsmList)

def vaccineData(dataframe):
    totPopolazioneItaliana = const.POP_ITA
    regionList = dataframe['nome_area'].unique().tolist()
    percentVaccinated = dataframe.groupby(['nome_area'])['seconda_dose'].apply(lambda x: (sum(x)/totPopolazioneItaliana)).tolist()
    totMale = dataframe.groupby(['nome_area'])['sesso_maschile'].sum().tolist()
    totFemale = dataframe.groupby(['nome_area'])['sesso_femminile'].sum().tolist()
    totPregressi = dataframe.groupby(['nome_area'])['pregressa_infezione'].sum().tolist()
    perEtaList = dataframe.groupby(['fascia_anagrafica','nome_area'])['seconda_dose'].sum().tolist()
    ivsmList = fetchIVSM()


    values = {
    'region' : sorted(regionList), 
    'percentVaccinated' : percentVaccinated,
    'eta1': perEtaList[0:21],
    'eta2': perEtaList[21:42],
    'eta3': perEtaList[42:63],
    'eta4': perEtaList[63:84],
    'eta5': perEtaList[84:105],
    'eta6': perEtaList[105:126],
    'eta7': perEtaList[126:147],
    'eta8': perEtaList[147:168],
    'eta9': perEtaList[168:],
    'male': totMale,
    'female': totFemale,
    'totPregressi':totPregressi,
    'IVSM' : ivsmList
    }

    newDf = pd.DataFrame(values)
    print(newDf['percentVaccinated'].sum())
    return(newDf)

secondaDose = preProcessing()
vaccines = vaccineData(secondaDose)

from sklearn.linear_model import LogisticRegression
features = ['IVSM']
X = vaccines[features]
y = vaccines['region']
lr_model = LogisticRegression()
#lr_model.fit(vaccines[['totPregressi','IVSM']].values.reshape(-1, 1), vaccines['percentVaccinated'].values.reshape(-1, 1))
lr_model.fit(X, y)
print(lr_model.predict(vaccines['eta6'].values.reshape(-1, 1)))"""
