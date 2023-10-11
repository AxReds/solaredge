# Import the pvoutput-ocf module
import pvoutput

# Create a PVOutput object with your own API key and system ID
pvo = pvoutput.PVOutput(api_key="3b41787f798ef111a3ad1a118f6a1fd0701b0397", system_id="97420")

# Open the text file in read mode
with open("import_file.txt", "r") as f:
#    # Read the lines of the file
    lines = f.readlines()

# Create an empty list to store the data to send
data = []

# For each line of the file
for line in lines:
    # Remove whitespace and split the line by commas
    line = line.strip().split(",")

    # Create a dictionary with keys corresponding to the parameters of the update status API
    record = {
        "d": line[0], # Date
        "g": line[1], # Energy generated
        "c": line[2], # Energy consumed
        # Add any other optional parameters
    }
    # Add the dictionary to the data list
data.append(record)

# Call the addbatchstatus method of the PVOutput object, passing the data list as an argument
response = pvo.addbatchstatus(data=data)

# Print the response with the status code and message
print(response)

# Handle any exceptions or errors
try:
    # Check if the response has a status code different from 200 (OK)
    response.raise_for_status()
except pvoutput.PVOutputError as e:
    # Print the exception
    print(e)
