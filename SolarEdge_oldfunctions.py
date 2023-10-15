# Function to get energy data and remove rows with null values
def get_energy_data_remove_nulls(url, file_name):
    response = requests.get(url)
    energy_data = response.json()
    data = [row['value'] for row in energy_data['energy']['values'] if row['value'] is not None]
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(["Date/Time;Value"])
        csvwriter.writerows([[row] for row in data])



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
