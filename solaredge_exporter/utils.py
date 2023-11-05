# Description: Utility functions for the SolarEdge API

#Built-in libraries
import csv
import os

#3rd party libraries
from datetime import datetime, timedelta

#Custom libraries
from .functions import *

# Function to get production data and replace null values with "0,0"
def SolarEdgeExportToFile(file_name: str, multiline_data: list): 
    #
    try:
        # Write data to the CSV file
        if not os.path.exists(file_name):
            with open(file_name, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(['Date/Time','Value']) # Write header if the file DOES NOT EXIST
                csvwriter.writerows(multiline_data)
        else:
            with open(file_name, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerows(multiline_data)
    except Exception as e:
        print(f"Error writing data to file: {e}")

#New Data Extraction Method
def getAllDataInPVOutFormat (ApiKey: str, SiteID: int, Operation: int, ExportFile: str, DataPeriod: str, StartYear: int, CurrentYear: int, LastUpdateDateTime: str):
    
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
            
            #Print the month to process
            print (f"Processing {year}-{str_month}")
            
            #Check what exporting process to execute
            if Operation == "1":
                SolarEdge_DataDictionary = call_PowerDetailed(ApiKey, SiteID, f"{year}-{str_month}", f"{year}-{str_month}-{last_day_of_month}")
            elif Operation == "2":
                SolarEdge_DataDictionary = call_SiteEnergy(ApiKey, SiteID, f"{year}-{str_month}-01", f"{year}-{str_month}-{last_day_of_month}", QuarterHour)
            elif Operation == "4":
                SolarEdge_DataDictionary = call_SitePower15mins(ApiKey, SiteID, f"{year}-{str_month}-01", f"{year}-{str_month}-{last_day_of_month}")
            elif Operation == "5":
                SolarEdge_DataDictionary = call_SiteEnergyDetailed(ApiKey, SiteID, f"{year}-{str_month}-01", f"{year}-{str_month}-{last_day_of_month}", Year)
            else:
                print ("Option not yet available")
                exit(1)
            
            #Export data to file
            SolarEdgeExportToFile (ExportFile, SolarEdge_DataDictionary)

