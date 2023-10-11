#https://powershelladministrator.com/2015/11/12/download-solaredge-solar-production-data-and-save-to-csv/

import requests
from datetime import datetime, timedelta
import os
import json
from SolarEdge_functions import *

# Read information from the JSON file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Access SolarEdge information in the JSON file to set constants values
SolarEdgeConfig = config_data['SolarEdge']
export_file = SolarEdgeConfig['OutputFile']
SolarEdge_SiteID = SolarEdgeConfig['SiteID']
SolarEdge_ApiKey = SolarEdgeConfig['ApiKey']

#Set other constants
Day = "DAY"
QuarterHour = "QUARTER_OF_AN_HOUR"
CurrentDate = datetime.now().strftime('%Y-%m-%d')
StartDate = CurrentDate
EndDate = CurrentDate
DataPeriodUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/dataPeriod?api_key={SolarEdge_ApiKey}"
OverviewUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/overview?api_key={SolarEdge_ApiKey}"
EnergyUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/energy?api_key={SolarEdge_ApiKey}"
DetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/details?api_key={SolarEdge_ApiKey}"

#
# Get site details and last update time from the overview API endpoint
#response_details = requests.get(OverviewUrl)
SiteDetails = requests.get(DetailsUrl).json()

response_Overview = requests.get(OverviewUrl).json()
SiteOverview = response_Overview['overview']

LastUpdateTime = SiteOverview['lastUpdateTime'].split()[0]
LastUpdateDateTime = datetime.strptime(LastUpdateTime, '%Y-%m-%d')

# Check if data needs to be downloaded based on last update time
if LastUpdateTime != CurrentDate:
    DaysAgo = (datetime.now() - LastUpdateDateTime).days
    if DaysAgo == 0:
        print("The energy data on the monitoring portal is up to date, will start downloading data if necessary")
    elif DaysAgo == 1:
        print("The energy data on the monitoring portal has not been updated for a day. "
              "This might have various reasons:\n"
              " - The update script is run within the first 15 minutes of a new day, in that case, it's usual behavior.\n"
              " - There has been an interruption in the connection between the inverter and the monitoring portal.\n"
              " - No data has been received on the monitoring portal.\n"
              "Script will continue as usual.")
    else:
        print(f"The installation has not been updated since {LastUpdateTime}. This is {DaysAgo} days ago. "
              "Script will continue, but it is advised to fix the error. "
              "This script will only download the data until the date of the last available data")

# Get data period information from the API endpoint
response_period = requests.get(DataPeriodUrl)
DataPeriod = response_period.json()
StartYear = datetime.strptime(DataPeriod['dataPeriod']['startDate'], '%Y-%m-%d').year
CurrentYear = datetime.now().year

# Loop through years and months to download energy data
for year in range(StartYear, CurrentYear + 1):
    if year == CurrentYear:
        if StartYear == CurrentYear:
            month = datetime.strptime(DataPeriod['dataPeriod']['startDate'], '%Y-%m-%d').month
        else:
            month = 1
        last_month = datetime.now().month if LastUpdateDateTime.month >= datetime.now().month else LastUpdateDateTime.month + 1
    else:
        if year == StartYear:
            month = datetime.strptime(DataPeriod['dataPeriod']['startDate'], '%Y-%m-%d').month
        else:
            month = 1
        last_month = 13

    for month in range(month, last_month):
        last_day_of_month = (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day
        str_month = "{:02d}".format(month)
        file_name = f"{year}{str_month} - {SiteDetails['details']['name']}{SolarEdge_SiteID}.csv"
        file_name_15min = f"{year}{str_month} - {SiteDetails['details']['name']}{SolarEdge_SiteID}-15min.csv"
        url_day = f"{EnergyUrl}&timeUnit={Day}&startDate={year}-{str_month}-01&endDate={year}-{str_month}-{last_day_of_month}"
        url_15min = f"{EnergyUrl}&timeUnit={QuarterHour}&startDate={year}-{str_month}-01&endDate={year}-{str_month}-{last_day_of_month}"
        
        if not os.path.exists(file_name):
            get_energy_data_remove_nulls(url_day, file_name)
        else:
            print(f"File {file_name} already exists. Script will not download this data again")
        
        if not os.path.exists(file_name_15min):
            get_energy_data_replace_nulls(url_15min, file_name_15min)
        else:
            print(f"File {file_name_15min} already exists. Script will not download this data again")

    if year < CurrentYear and year >= LastUpdateDateTime.year:
        url_year = f"{EnergyUrl}&timeUnit={Day}&startDate={year}-01-01&endDate={year}-12-31"
        file_name_year = f"{year} - {SiteDetails['details']['name']}{SolarEdge_SiteID}.csv"
        if not os.path.exists(file_name_year):
            get_energy_data_remove_nulls(url_year, file_name_year)
        else:
            print(f"File {file_name_year} already exists. Script will not download this data again")
