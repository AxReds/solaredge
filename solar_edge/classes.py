# Description: This module contains all classes used to deal with SolarEdge API

# Import built-in libraries
from datetime import datetime

# Import 3rd party libraries
import requests

# Import custom libraries
from solar_edge.functions import call_SiteDetails, call_SiteOverview



# SolarEdgeSiteData class
class SolarEdgeSiteData:
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

        # Get site details and last update time from the site details API endpoint
        site_details = call_SiteDetails(self.api_key, self.site_id)
        self.name = site_details['details']['name']
        self.status = site_details['details']['status']
        self.account_id = site_details['details']['accountId']
        self.peak_power = site_details['details']['peakPower']
        self.installation_date = site_details['details']['installationDate']
        self.currency = site_details['details']['currency']

        # Get site overview information from the overview API endpoint
        overview = call_SiteOverview (self.api_key, self.site_id)
        self.last_update_time = overview['overview']['lastUpdateTime']
        self.lifetime_energy = overview['overview']['lifeTimeData']['energy']
        self.lifetime_revenues = overview['overview']['lifeTimeData']['revenue']
        self.last_Year_Energy = overview['overview']['lastYearData']['energy']
        self.last_Month_Energy = overview['overview']['lastMonthData']['energy']
        self.last_Day_Energy = overview['overview']['lastDayData']['energy']
        self.current_Power = overview['overview']['currentPower']['power']

# PVOutputStatus class
class PVOutputStatus:
    def __init__(self, api_key: str, system_id: str, energy_generation: float, power_generation: float,
                    energy_consumption: float, power_consumption: float, temperature: float, voltage: float,
                    extended_data: dict):
        self.api_key = api_key
        self.system_id = system_id
        self.energy_generation = energy_generation
        self.power_generation = power_generation
        self.energy_consumption = energy_consumption
        self.power_consumption = power_consumption
        self.temperature = temperature
        self.voltage = voltage
        self.extended_data = extended_data

    def add_status(self):
        # Get the current date and time
        now = datetime.now()
        date = now.strftime('%Y%m%d')
        time = now.strftime('%H:%M')

        # Build the request parameters
        params = {
            'd': date,
            't': time,
            'v1': self.energy_generation,
            'v2': self.power_generation,
            'v3': self.energy_consumption,
            'v4': self.power_consumption,
            'v5': self.temperature,
            'v6': self.voltage,
            'c1': self.extended_data.get('c1', ''),
            'c2': self.extended_data.get('c2', ''),
            'c3': self.extended_data.get('c3', ''),
            'c4': self.extended_data.get('c4', ''),
            'c5': self.extended_data.get('c5', ''),
            'c6': self.extended_data.get('c6', ''),
            'c7': self.extended_data.get('c7', ''),
            'c8': self.extended_data.get('c8', ''),
            'c9': self.extended_data.get('c9', ''),
            'c10': self.extended_data.get('c10', ''),
            'data': 0,
            'delay': 0,
            'x': 0,
            'm1': '',
            'm2': ''
        }

        # Send the request to the PVOutput API
        url = f'https://pvoutput.org/service/r2/addstatus.jsp?key={self.api_key}&sid={self.system_id}'
        response = requests.post(url, params=params)

        # Check the response status code
        if response.status_code != 200:
            raise Exception(f'Error adding status: {response.text}')

    def get_extended_data_key(self, key: str) -> str:
        # Define the extended data keys
        extended_data_keys = {
            'v7': 'c1',
            'v8': 'c2',
            'v9': 'c3',
            'v10': 'c4',
            'v11': 'c5',
            'v12': 'c6',
            'v13': 'c7',
            'v14': 'c8',
            'v15': 'c9',
            'v16': 'c10'
        }

        # Return the corresponding extended data key number
        return extended_data_keys.get(key, '')
