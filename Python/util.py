import os
import urllib.request

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
