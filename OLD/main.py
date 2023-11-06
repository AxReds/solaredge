#https://powershelladministrator.com/2015/11/12/download-solaredge-solar-production-data-and-save-to-csv/

#bilt-in imports
import json, os
import requests

#3rd party imports
from datetime import datetime

#custom imports
from solaredge_exporter import SolarEdgeSiteData, getAllDataInPVOutFormat


# Main function ==> all variables would be local to this function
def main():

    #Clear screen depending on OS
    os.system("cls" if os.name == "nt" else "clear")


    # Read information from the JSON file
    try:
        with open('config.json', 'r') as config_file:
            SolarEdgeConfig = json.load(config_file)['SolarEdge']
    except FileNotFoundError:
        print("Error: config.json file not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: config.json file is not valid JSON.")
        exit(1)


    # Access SolarEdge information in the JSON file to set constants values
    SolarEdge_ExportFile = SolarEdgeConfig['OutputFile']
    SolarEdge_SiteID = int(SolarEdgeConfig['SiteID'])
    SolarEdge_ApiKey = SolarEdgeConfig['ApiKey']

    DataPeriodUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/dataPeriod?api_key={SolarEdge_ApiKey}"
    # Get data period information from the API endpoint
    response_period = requests.get(DataPeriodUrl)
    DataPeriod = response_period.json()
    StartYear = datetime.strptime(DataPeriod['dataPeriod']['startDate'], '%Y-%m-%d').year
    CurrentYear = datetime.now().year


    # Get site details from SolarEdge API
    SiteDetails = SolarEdgeSiteData (SolarEdge_SiteID, SolarEdge_ApiKey)
    LastUpdateTime = SiteDetails.last_update_time.split()[0]
    LastUpdateDateTime = datetime.strptime(LastUpdateTime, '%Y-%m-%d')

    # Check if data needs to be downloaded based on last update time
    DaysAgo = (datetime.now() - LastUpdateDateTime).days
    if DaysAgo == 0:
        print("The energy data on the monitoring portal is up to date."
            "The program can continue.")
    elif DaysAgo == 1:
        print("The energy data on the monitoring portal has not been updated for a day."
            "This could be due to various reasons:\n"
            " - The update script runs within the first 15 minutes of a new day; in that case, it's normal behavior.\n"
            " - There might have been an interruption in the connection between the inverter and the monitoring portal.\n"
            " - No data has been received on the monitoring portal.\n"
            "The program can continue, but please investigate.")
    else:
        print(f"The installation has not been updated since {LastUpdateTime}. This is {DaysAgo} days ago. "
            "Script will continue, but it is advised to fix the error. "
            "This script will only download the data until the date of the last available data")


    # Print site details
    print(f"\n\nSolareEdge Site {SolarEdge_SiteID} has the following details:\n"
            f" - Name:              {SiteDetails.name}\n"
            f" - Account ID:        {SiteDetails.account_id}\n"
            f" - Status:            {SiteDetails.status}\n"
            f" - Peak Power:        {SiteDetails.peak_power}\n"
            f" - Installed on:      {SiteDetails.installation_date}\n"
            f" - Total Energy:      {SiteDetails.lifetime_energy}\n"
            f" - Total Revenues:    {SiteDetails.lifetime_revenues} {SiteDetails.currency}\n"
            f" - Last Update:       {SiteDetails.last_update_time}\n"
            f" - Last Year Energy:  {SiteDetails.last_Year_Energy}\n"
            f" - Last Month Energy: {SiteDetails.last_Month_Energy}\n"
            f" - Last Day Energy:   {SiteDetails.last_Day_Energy}\n"
            f" - Current Power:     {SiteDetails.current_Power}\n")

    # Collect user choice
    choice = input("Please select an export method and press <enter> to confirm:\n"
            "1 - Export Daily Power Production (15mins interval)\n"
            "2 - Export Daily Energy Production (15mins interval)\n"
            "\n")

    # Invoke the proper function to get the data based on user choice
    if choice == "1":
        getAllDataInPVOutFormat (SolarEdge_ApiKey, SolarEdge_SiteID, choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, LastUpdateDateTime)
        print("Export Completed")
    elif choice == "2":
        getAllDataInPVOutFormat (SolarEdge_ApiKey, SolarEdge_SiteID, choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, LastUpdateDateTime)
        print("Export Completed")
    elif choice == "3":
        print("Il pianeta è stato distrutto!")
    elif choice == "4":
        getAllDataInPVOutFormat (SolarEdge_ApiKey, SolarEdge_SiteID, choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, LastUpdateDateTime)
        print("Export Completed")
    elif choice == "5":
        getAllDataInPVOutFormat (SolarEdge_ApiKey, SolarEdge_SiteID, choice, SolarEdge_ExportFile, DataPeriod, StartYear, CurrentYear, LastUpdateDateTime)
        print("Export Completed")
    else:
        exit(0)

#kickstart the program
if __name__ == "__main__":
    main()