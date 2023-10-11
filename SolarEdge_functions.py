#Import Declaration
import requests
import csv

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

# Function to get energy data and replace null values with "0,0"
def get_energy_data_replace_nulls(url, file_name):
    response = requests.get(url)
    energy_data = response.json()
    #
    #Replace null values with "0,0"
    for row in energy_data['energy']['values']:
        if row['value'] is None:
            row['value'] = "0,0"

    data = [[row['value']] for row in energy_data['energy']['values']]
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(["Date/Time;Value"])
        csvwriter.writerows(data)
