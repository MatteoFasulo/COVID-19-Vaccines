import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import constants as const

import util

def main():
  """
  """
  # Setup Seaborn plot settings
  sns.set(style="white")
  sns.set(style="whitegrid", color_codes=True)
  sns.set(rc={'figure.figsize':(11.7,13.27)})

  # Get latest vaccine report from Protezione Civile
  util.getLatestVaccineReport()

  # Load the dataset using Pandas and plot first chart
  fullDF = util.loadVaccines()
  fullDF.groupby("fornitore")["prima_dose"].sum().plot.pie(autopct='%.2f%%',
                                                         ylabel='',
                                                         title='Percentage of first doses by manufacturer')
  plt.savefig('1st_dose.png')

  # Clean the dataset for all the following analysis
  vaccinati = util.preProcessing(fullDF)
  vaccinati.groupby("fornitore")["seconda_dose"].sum().plot.pie(autopct='%.2f',
                                                                ylabel='',
                                                                title='Percentage of second doses (vaccinated) by manufacturer')
  plt.savefig('2st_dose.png')

  sns.set(rc={'figure.figsize':(16,8)})
  vaccinati.groupby(["nome_area","fornitore"])["seconda_dose"].sum().unstack().plot.bar(xlabel='Regione',
                                                                                        title='Vaccine manufacturer by region')
  plt.savefig('vaccine_x_manufacturer.png')

  sns.set(rc={'figure.figsize':(16,8)})
  vaccinati.groupby(["fascia_anagrafica","fornitore"])["seconda_dose"].sum().unstack().plot.bar(xlabel="Fascia di età",
                                                                                                title='Vaccine manufacturer by age group')
  plt.savefig('vaccine_x_age.png')
  
  sns.set(rc={'figure.figsize':(20,50)})
  vaccinati.groupby(["nome_area","fascia_anagrafica","fornitore"])["seconda_dose"].sum().unstack().plot(kind='barh', stacked=True,
                                                                                                        ylabel="Regione, Fascia di età",
                                                                                                        title='Vaccine manufacturer by region and age group')
  plt.savefig('vaccine_x_region_and_age.png')

  totOver12 = const.POP_ITA - const.POP_ITA_U12
  vaccinati.groupby(['nome_area'])['seconda_dose'].apply(lambda x: (sum(x)/totOver12)*100)

  dictFactorsDF = util.SVI()
  finalDF = pd.merge(dictFactorsDF, vaccinati, left_index=True, right_on='codice_regione_ISTAT')
  finalDF['coverage'] = finalDF.apply(lambda x: (x.tot_Dosi/x.residenti), axis=1)
  finalDF = finalDF[['data_somministrazione', 'seconda_dose', 'tot_Dosi', 'residenti', 'coverage', 'fascia_anagrafica', 'fornitore', 'codice_regione_ISTAT','nome_area','PIL','mono_Family','six_more_Family','low_Educ','ass_Unease','house_Crow','u30_Unemployed','eco_Unease']]
  finalDF = finalDF.reset_index(drop=True)
  finalDF.describe()


if __name__ == "__main__":
  main()
