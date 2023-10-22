# SolarEdge_functions.py

This module provides functions for interacting with the SolarEdge API.

## Purpose

The purpose of this module is to provide a set of functions that can be used to interact with the SolarEdge API. The functions in this module can be used to retrieve data from a SolarEdge site, such as power production data, site information, and more.

## Functions

### `get_SiteData(url:str, size: int = 100, startIndex: int = 0, searchText: str = 'Name', sortProperty: str = 'Name', sortOrder: str ='ASC', Status: str = 'All') -> list`

This function retrieves site data from the SolarEdge API and returns it as a list. The function takes the following parameters:

- `url`: The URL of the SolarEdge API endpoint to retrieve the site data from.
- `size`: The number of items to retrieve per page (default: 100).
- `startIndex`: The index of the first item to retrieve (default: 0).
- `searchText`: The text to search for in the site data (default: 'Name').
- `sortProperty`: The property to sort the site data by (default: 'Name').
- `sortOrder`: The order to sort the site data in ('ASC' or 'DESC', default: 'ASC').
- `Status`: The status of the site data to retrieve ('All', 'Active', or 'Inactive', default: 'All').

### `get_PowerDetails(url:str) -> dict`

This function retrieves power production data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the power production data from.

### `get_Inventory(url:str) -> dict`

This function retrieves inventory data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the inventory data from.

### `get_EnvironmentalBenefits(url:str) -> dict`

This function retrieves environmental benefits data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the environmental benefits data from.

### `get_Overview(url:str) -> dict`

This function retrieves overview data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the overview data from.

### `get_EnergyDetails(url:str) -> dict`

This function retrieves energy details data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the energy details data from.

### `get_StorageData(url:str) -> dict`

This function retrieves storage data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the storage data from.

### `get_MeterData(url:str) -> dict`

This function retrieves meter data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the meter data from.

### `get_ExtendedData(url:str) -> dict`

This function retrieves extended data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the extended data from.

### `get_Events(url:str) -> dict`

This function retrieves events data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the events data from.

### `get_Alerts(url:str) -> dict`

This function retrieves alerts data from the SolarEdge API and returns it as a dictionary. The function takes the following parameter:

- `url`: The URL of the SolarEdge API endpoint to retrieve the alerts data from.
