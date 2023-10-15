#https://powershelladministrator.com/2015/11/12/download-solaredge-solar-production-data-and-save-to-csv/

import requests
from datetime import datetime, timedelta
import json, os
from SolarEdge_functions import *

# Read information from the JSON file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Access SolarEdge information in the JSON file to set constants values
SolarEdgeConfig = config_data['SolarEdge']
SolarEdge_ExportFile = SolarEdgeConfig['OutputFile']
SolarEdge_SiteID = SolarEdgeConfig['SiteID']
SolarEdge_ApiKey = SolarEdgeConfig['ApiKey']

#Set other constants
CurrentDate = datetime.now().strftime('%Y-%m-%d')
StartDate = CurrentDate
EndDate = CurrentDate
DataPeriodUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/dataPeriod?api_key={SolarEdge_ApiKey}"
OverviewUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/overview?api_key={SolarEdge_ApiKey}"
EnergyUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/energy?api_key={SolarEdge_ApiKey}"
DetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/details?api_key={SolarEdge_ApiKey}"
PowerDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/powerDetails?api_key={SolarEdge_ApiKey}"

# Get data period information from the API endpoint
response_period = requests.get(DataPeriodUrl)
DataPeriod = response_period.json()
StartYear = datetime.strptime(DataPeriod['dataPeriod']['startDate'], '%Y-%m-%d').year
CurrentYear = datetime.now().year

#
# Get site details and last update time from the overview API endpoint
#response_details = requests.get(OverviewUrl)
SiteDetails = requests.get(DetailsUrl).json()

SolarEdge_SiteName = SiteDetails['details']['name']
SolarEdge_Status = SiteDetails['details']['status']
SolarEdge_AccountID = SiteDetails['details']['accountId']
SolarEdge_Status = SiteDetails['details']['status']
SolarEdge_PeakPower = SiteDetails['details']['peakPower']
SolarEdge_installationDate = SiteDetails['details']['installationDate']
SolarEdge_Currency = SiteDetails['details']['currency']

response_Overview = requests.get(OverviewUrl).json()
SiteOverview = response_Overview['overview']
SolarEdge_lifeTimeData_Energy = SiteOverview['lifeTimeData']['energy']
SolarEdge_lifeRevenue_Energy = SiteOverview['lifeTimeData']['revenue']

LastUpdateTime = SiteOverview['lastUpdateTime'].split()[0]
LastUpdateDateTime = datetime.strptime(LastUpdateTime, '%Y-%m-%d')


os.system("cls" if os.name == "nt" else "clear")
print(f"\n\nSolareEdge Site {SolarEdge_SiteID} owned by {SolarEdge_SiteName} has the following details:\n"
        f" - Account ID:     {SolarEdge_AccountID}\n"
        f" - Status:         {SolarEdge_Status}\n"
        f" - Peak Power:     {SolarEdge_PeakPower}\n"
        f" - Installed on:   {SolarEdge_installationDate}\n"
        f" - Total Energy:   {SolarEdge_lifeTimeData_Energy}\n"
        f" - Total Revenues: {SolarEdge_lifeRevenue_Energy} {SolarEdge_Currency} \n"
        "\n")

choice = input("Please select an export method and press <enter> to confirm:\n"
        "1 - Export Daily Power Production (15mins interval)\n"
        "2 - Export Daily Energy Production (15mins interval)\n"
        "\n")

if choice == "1":
    #getAllData (DataPeriod, StartYear, CurrentYear, SiteDetails, SolarEdge_SiteID, EnergyUrl, LastUpdateTime, LastUpdateDateTime)
    getAllDataPVOutFormat (choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, PowerDetailsUrl, LastUpdateDateTime)
    print("Export Completed")
elif choice == "2":
    getAllDataPVOutFormat (choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, EnergyUrl, LastUpdateDateTime)
    print("Export Completed")
elif choice == "3":
    print("Il pianeta è stato distrutto!")
    # Inserisci qui il codice per l'opzione 3
else:
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