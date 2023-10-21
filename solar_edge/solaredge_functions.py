# Description: This module contains functions to call the SolarEdge API and return the data in JSON format (most of the time).

#Built-in libraries
import requests

#3rd party libraries

#Custom libraries


#Set Constants based on the API documentation
QuarterHour = "QUARTER_OF_AN_HOUR"
Hour = "HOUR"
Day = "DAY"
Week = "WEEK"
Month =  "MONTH"
Year = "YEAR"

# This block is executed when the module runs directly
if __name__ == "__main__":
    print ("This is a library and cannot be ran standalone.")

# Function returns a list of sites related to the given token, which is the account api_key.
# The API accepts parameters for convenient search, sort and pagination.
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

# Function returns site details and return a JSON
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

# Function returns the production start and end dates of the site
def call_SiteData_Start_End_Dates(SolarEdge_ApiKey: str, SolarEdge_SiteID: int) -> list:
    #Set Constant URL
    SiteDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/dataPeriod?api_key={SolarEdge_ApiKey}"
   
    #Call api and get site details 
    response = requests.get(SiteDetailsUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return
    
    SiteDetails = response.json()
    return (SiteDetails)

# Function returns the production start and end dates for all the site owned by the account
def call_SiteData_Bulk_Start_End_Dates(SolarEdge_ApiKey: str, SolarEdge_SiteIDs: str) -> list:
    #Set Constant URL
    SiteDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteIDs}/dataPeriod?api_key={SolarEdge_ApiKey}"
   
    #Call api and get site details 
    response = requests.get(SiteDetailsUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return
    
    SiteDetails = response.json()
    return (SiteDetails)

# Function returns the site energy measurements and replaces null values with "0.0"
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

# Function returns the site total energy produced for a given period and returns a JSON
def call_SiteEnergy_TimePeriod(SolarEdge_ApiKey: str, SolarEdge_SiteID: int, startDate: str, endDate: str) -> list:
 #Check if timeUnit is valid

    #Set Constant URL
    EnergyUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/timeFrameEnergy?api_key={SolarEdge_ApiKey}&startDate={startDate}&endDate={endDate}"
    
    # Make a GET request to the specified URL
    response = requests.get(EnergyUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return

    # Parse the JSON response
    energy_data = response.json()

# Function returns the site power measurements in 15 minutes resolution and replaces null values with "0,0"
def call_SitePower15mins(SolarEdge_ApiKey: str, SolarEdge_SiteID: int, startTime: str, endTime: str) -> list:
 #Check if timeUnit is valid

    #Set Constant URL
    EnergyUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/power?api_key={SolarEdge_ApiKey}&startTime={startTime}%2000:00:00&endTime={endTime}%2023:59:59"
    
    # Make a GET request to the specified URL
    response = requests.get(EnergyUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return

    #Initialize an empty list to store multiline data
    multiline_data = []

    # Parse the JSON response
    energy_data = response.json()

    # Access nested data in the JSON
    meter_telemetries = energy_data['power']['values']

    #
    # Replace null values with "0.0" and create multiline data
    for meter_telemetry in meter_telemetries:
        date = meter_telemetry['date']
        value = '0.0' if meter_telemetry['value'] is None else meter_telemetry['value']
        
        # Create a multiline list with 'date' and 'value' and append it to multiline_data
        data = [date, value]
        multiline_data.append(data)
    
    return (multiline_data)

# Function returns the site overview information and returns a JSON
def call_SiteOverview (SolarEdge_ApiKey: str, SolarEdge_SiteID: int) -> list:
    #Set Constant URL
    OverviewUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/overview?api_key={SolarEdge_ApiKey}"
    
    # Make a GET request to the specified URL
    response = requests.get(OverviewUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return

    # Parse the JSON response
    overview_data = response.json()
    
    return (overview_data)

# Function returns production data and replaces null values with "0.0"
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

def call_SiteEnergyDetailed(SolarEdge_ApiKey: str, SolarEdge_SiteID: int, startTime: str, endTime: str, timeUnit: str ="DAY", meters: str = None) -> list:
    #Set Constant URL
    EnergyDetailsUrl = f"https://monitoringapi.solaredge.com/site/{SolarEdge_SiteID}/energyDetails?api_key={SolarEdge_ApiKey}&startTime={startTime}%2000:00:00&endTime={endTime}%2023:59:59&timeUnit={timeUnit}"
    
    # Check if meters is not None and add it to the URL if it is not None
    if meters is not None:
        EnergyDetailsUrl += f"&meters={meters}"
 
    # Make a GET request to the specified URL
    response = requests.get(EnergyDetailsUrl)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error in the request: {response.status_code}")
        return

    # Parse the JSON response
    energy_data = response.json()
    
    return (energy_data)
