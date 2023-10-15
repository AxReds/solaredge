#Import Declaration
import requests
import csv
from datetime import datetime, timedelta
import os

#Set Constants
Day = "DAY"
QuarterHour = "QUARTER_OF_AN_HOUR"

#
# This block is executed when the module is run directly
if __name__ == "__main__":
    # Test some examples
    print ("This is a library and cannot be ran standalone.")

#
# Function to get production data and replace null values with "0,0"
def get_Power_data(url):
    
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
    
    return (multiline_data)

#
# Function to get production data and replace null values with "0,0"
def SolarEdge_ExportToFile(file_name, multiline_data): 
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

#
# Function to get production data and replace null values with "0,0"
def get_Energy_data(url):
    
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
    meter_telemetries = energy_data['energy']['values']

    #
    # Replace null values with "0.0" and create multiline data
    for meter_telemetry in meter_telemetries:
        date = meter_telemetry['date']
        if meter_telemetry['value'] is None:
            value = 0.0
        else:
            value = meter_telemetry['value']

        
        # Create a multiline list with 'date' and 'value' and append it to multiline_data
        data = [date, value]
        multiline_data.append(data)
    
    return (multiline_data)


#
#New Data Extraction Method
def getAllDataPVOutFormat (Operation, ExportFile, DataPeriod, StartYear, CurrentYear, EnergyUrl, LastUpdateDateTime):
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
            
            #Check what exporting process to execute
            if Operation == "1":
                url_15min = f"{EnergyUrl}&meters=PRODUCTION&timeUnit={QuarterHour}&startTime={year}-{str_month}-01 00:00:00&endTime={year}-{str_month}-{last_day_of_month} 23:59:59"
                SolarEdge_DataDictionary = get_Power_data(url_15min)
            elif Operation == "2":
                url_15min = f"{EnergyUrl}&timeUnit={QuarterHour}&startDate={year}-{str_month}-01&endDate={year}-{str_month}-{last_day_of_month}"
                SolarEdge_DataDictionary = get_Energy_data(url_15min)
            else:
                print ("Option not yet available")
            
            #Export data to file
            SolarEdge_ExportToFile (ExportFile, SolarEdge_DataDictionary)

            
