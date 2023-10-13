#Import Declaration
import requests
import csv
from datetime import datetime, timedelta
import os
import json

#Set Constants
Day = "DAY"
QuarterHour = "QUARTER_OF_AN_HOUR"

# This block is executed when the module is run directly
if __name__ == "__main__":
    # Test some examples
    print ("This is a library and cannot be ran standalone.")

# Function to get energy data and remove rows with null values
def get_energy_data_remove_nulls(url, file_name):
    response = requests.get(url)
    energy_data = response.json()
    data = [row['value'] for row in energy_data['energy']['values'] if row['value'] is not None]
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(["Date/Time;Value"])
        csvwriter.writerows([[row] for row in data])

# Function to get production data and replace null values with "0,0"
def get_production_data(url, file_name):
    
    #Initialize an empty list to store multiline data
    multiline_data = []
    
    # Make a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return

    # Parse the JSON response
    energy_data = response.json()
    
    # Access nested data in the JSON
    meter_telemetries = energy_data['powerDetails']['meters'][0]['values']

    #
    # Replace null values with "0.0" and create multiline data
    for meter_telemetry in meter_telemetries:
        date = meter_telemetry['date']
        value = meter_telemetry.get('value', '0.0')
        
        # Create a multiline list with 'date' and 'value' and append it to multiline_data
        data = [date, value]
        multiline_data.append(data)
    
    #
    # Write data to the CSV file
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            csvwriter.writerow(['Date/Time','Value']) # Write header if the file DOES NOT EXIST
            csvwriter.writerows(multiline_data)
    else:
        with open(file_name, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            #csvwriter.writerow(['Date/Time','Value']) # DOES NOT Write header if the file EXIST
            csvwriter.writerows(multiline_data)
            

# Original Extraction Method
def getAllData (DataPeriod, 
                StartYear, 
                CurrentYear, 
                SiteDetails, 
                SolarEdge_SiteID, 
                EnergyUrl,
                LastUpdateTime,
                LastUpdateDateTime):
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

#New Data Extraction Method
def getAllDataPVOutFormat (ExportFile, DataPeriod, StartYear, CurrentYear, EnergyUrl, LastUpdateDateTime):
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


            url_15min = f"{EnergyUrl}&meters=PRODUCTION&timeUnit={QuarterHour}&startTime={year}-{str_month}-01 00:00:00&endTime={year}-{str_month}-{last_day_of_month} 23:59:59"
            get_production_data(url_15min, ExportFile)

            #if not os.path.exists(ExportFile):
            #    get_production_data(url_15min, ExportFile)
            #else:
            #    print(f"File {ExportFile} already exists. Script will not download this data again")
