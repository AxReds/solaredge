#Import Declaration
import requests
import csv
from datetime import datetime, timedelta
import os

#
#Set Constants based on the API documentation
QuarterHour = "QUARTER_OF_AN_HOUR"
Hour = "HOUR"
Day = "DAY"
Week = "WEEK"
Month = "MONTH"
Year = "YEAR"

#
# This block is executed when the module is run directly
if __name__ == "__main__":
    # Test some examples
    print ("This is a library and cannot be ran standalone.")


# SolarEdge_SiteData class
class SolarEdge_SiteData:
    def __init__(self, site_id: int, api_key: str):
        
        # Initialize the class variables
        self.site_id = site_id
        self.api_key = api_key
        self.name = None
        self.status = None
        self.account_id = None
        self.peak_power = None
        self.installation_date = None
        self.currency = None
        self.last_update_time = None
        self.lifetime_energy = None
        self.lifetime_revenues = None
        self.last_Year_Energy = None
        self.last_Month_Energy = None
        self.last_Day_Energy = None
        self.current_Power = None

        #
        # Get site details and last update time from the site details API endpoint
        site_details = call_SiteDetails(self.api_key, self.site_id)
        self.name = site_details['details']['name']
        self.status = site_details['details']['status']
        self.account_id = site_details['details']['accountId']
        self.peak_power = site_details['details']['peakPower']
        self.installation_date = site_details['details']['installationDate']
        self.currency = site_details['details']['currency']

        # Get site overview information from the overview API endpoint
        overview = self.call_Overview()
        self.last_update_time = overview['overview']['lastUpdateTime']
        self.lifetime_energy = overview['overview']['lifeTimeData']['energy']
        self.lifetime_revenues = overview['overview']['lifeTimeData']['revenue']
        self.last_Year_Energy = overview['overview']['lastYearData']['energy']
        self.last_Month_Energy = overview['overview']['lastMonthData']['energy']
        self.last_Day_Energy = overview['overview']['lastDayData']['energy']
        self.current_Power = overview['overview']['currentPower']['power']

    def call_Overview(self):
        url = f"https://monitoringapi.solaredge.com/site/{self.site_id}/overview?api_key={self.api_key}"
        response = requests.get(url)
        return response.json()

# Function to get sites data and return a list
def call_SiteList(SolarEdge_ApiKey: str, size: int = 100, startIndex: int = 0, searchText: str = 'Name', sortProperty: str = 'Name', sortOrder: str ='ASC', Status: str = 'All') -> list:
    #Check if searchText is valid
    ALLOWED_SEARCH_TEXT = ["Name","Notes", "Address", "City", "Zip code", "Full address",  "Country"]
    if searchText not in ALLOWED_SEARCH_TEXT:
        raise ValueError(f"timeUnit must be one of {ALLOWED_SEARCH_TEXT}")
    
    #Check if sortProperty is valid
    ALLOWED_SORT_PROPERTY = ["Name","Country", "State", "City", "Address","Notes", "Address", "City", "Zip code", "Status",  "PeakPower", "InstallationDate", "Amount","MaxSeverity", "CreationTime"]
    if sortProperty not in ALLOWED_SORT_PROPERTY:
        raise ValueError(f"timeUnit must be one of {ALLOWED_SORT_PROPERTY}")
    
    #Check if sortOrder is valid
    ALLOWED_SORT_ORDER = ["ASC","DESC"]
    if sortOrder not in ALLOWED_SORT_ORDER:
        raise ValueError(f"timeUnit must be one of {ALLOWED_SORT_ORDER}")
    
    #Check if Status is valid
    ALLOWED_STATUS = ["All","Active", "Pending", "Disabled"]
    if Status not in ALLOWED_STATUS:
        raise ValueError(f"timeUnit must be one of {ALLOWED_STATUS}")

    # Set Constant URL
    SiteDataUrl = f"https://monitoringapi.solaredge.com/sites/list?api_key={SolarEdge_ApiKey}"
    # Compose the URL
    url = f"{SiteDataUrl}&size={size}&startIndex={startIndex}&searchText={searchText}&sortProperty={sortProperty}&sortOrder={sortOrder}&Status={Status}"

    # Initialize an empty list to store multiline data
    multiline_data = []
    

    # Make a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        exit(1)

    # Parse the JSON response
    response_data = response.json()
    
    # Access nested data in the JSON
    site_details = response_data['sites']
    
    #Create multiline data with the site details
    for site_detail in site_details['site']:
        site_id = site_detail['id']
        site_name = site_detail['name']
        site_accountId = site_detail['accountId']
        site_status = site_detail['status']
        site_peakPower = site_detail['peakPower']
        site_currency = site_detail['currency']
        site_installationDate = site_detail['installationDate']
        site_ptoDate = site_detail['ptoDate']
        site_notes = site_detail['notes']
        site_type = site_detail['type']
        site_location_country = site_detail['location']['country']
        try:
            site_location_state = site_detail['location']['state']
        except:
            site_location_state = ""
        site_location_city = site_detail['location']['city']
        site_location_address = site_detail['location']['address']
        site_location_address2 = site_detail['location']['address2']
        site_location_zip = site_detail['location']['zip']
        site_location_timeZone = site_detail['location']['timeZone']
        try:
            site_alertQuantity = site_detail['alertQuantity']
        except:
            site_alertQuantity = "0"
        try:
            site_alertSeverity = site_detail['alertSeverity']
        except:
            site_alertSeverity = "NONE"
        try:
            site_uris_PUBLIC_URL = site_detail['uris']['PUBLIC_URL']
        except:
            site_uris_PUBLIC_URL = ""
        site_uris_SITE_IMAGE = site_detail['uris']['SITE_IMAGE']
        site_uris_DATA_PERIOD = site_detail['uris']['DATA_PERIOD']
        site_uris_DETAILS = site_detail['uris']['DETAILS']
        site_uris_OVERVIEW = site_detail['uris']['OVERVIEW']
        try:
            site_publicSettings_name = site_detail['publicSettings']['name']
        except:
            site_publicSettings_name = ""
        try:
            site_publicSettings_isPublic = site_detail['publicSettings']['isPublic']
        except:
            site_publicSettings_isPublic = "false"
        
        data = [site_id, site_name, site_accountId, 
                site_status, site_peakPower, site_currency, 
                site_installationDate, site_ptoDate, site_notes, 
                site_type, site_location_country, site_location_state, 
                site_location_city, site_location_address, site_location_address2, 
                site_location_zip, site_location_timeZone, site_alertQuantity, 
                site_alertSeverity, site_uris_PUBLIC_URL, site_uris_SITE_IMAGE, 
                site_uris_DATA_PERIOD, site_uris_DETAILS, site_uris_OVERVIEW,
                site_publicSettings_name, site_publicSettings_isPublic]
        multiline_data.append(data)
    return (multiline_data)

#Function to get site details and return a list
def call_SiteDetails(SolarEdge_ApiKey: str, SolarEdge_SiteID:int) -> list:
    #Set Constant URL
    SiteDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/details?api_key={SolarEdge_ApiKey}"
   
    #Call api and get site details 
    response = requests.get(SiteDetailsUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return
    
    SiteDetails = response.json()
    return (SiteDetails)

# Function to get production data and replace null values with "0,0"
def call_PowerDetailed(SolarEdge_ApiKey: str, SolarEdge_SiteID: int, startTime: str, endTime: str, meters: str = "PRODUCTION") -> list:
    #Set Constant URL
    PowerDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/powerDetails?api_key={SolarEdge_ApiKey}&startTime={startTime}-01%2000:00:00&endTime={endTime}%2023:59:59&meters={meters}"

    #Initialize an empty list to store multiline data
    multiline_data = []
    
    # Make a GET request to the specified URL
    response = requests.get(PowerDetailsUrl)
    
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

# Function to get production data and replace null values with "0,0"
def call_SiteEnergy(SolarEdge_ApiKey: str, SolarEdge_SiteID: int, startDate: str, endDate: str, timeUnit: str = Day) -> list:
    #Check if timeUnit is valid
    ALLOWED_TIME_UNITS = ["QUARTER_OF_AN_HOUR","HOUR", "DAY", "WEEK", "MONTH", "YEAR"]
    if timeUnit not in ALLOWED_TIME_UNITS:
        raise ValueError(f"timeUnit must be one of {ALLOWED_TIME_UNITS}")

    #Set Constant URL
    EnergyUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/energy?api_key={SolarEdge_ApiKey}&timeUnit={timeUnit}&startDate={startDate}&endDate={endDate}"

    #Initialize an empty list to store multiline data
    multiline_data = []
    
    # Make a GET request to the specified URL
    response = requests.get(EnergyUrl)
    
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

# Function to get production data and replace null values with "0,0"
def SolarEdge_ExportToFile(file_name: str, multiline_data: list): 
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
def getAllDataPVOutFormat (ApiKey: str, SiteID: int, Operation: int, ExportFile: str, DataPeriod: str, StartYear: int, CurrentYear: int, LastUpdateDateTime: str):
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
            else:
                print ("Option not yet available")
                exit(1)
            
            #Export data to file
            SolarEdge_ExportToFile (ExportFile, SolarEdge_DataDictionary)

