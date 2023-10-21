#Import Declaration
import requests

#Constants Declaration
pvout_webapi_url = "https://pvoutput.org/service/r2/addstatus.jsp"

#functions definition for PVOutput.org data import 
#
def PVOut_AddStatusService (pvout_Apikey, 
                            pvout_SystemId, 
                            pvout_Payload):
    pvout_Headers = {
    "X-Pvoutput-Apikey": pvout_Apikey,
    "X-Pvoutput-SystemId": pvout_SystemId,
    }
    
    
    response = requests.post(pvout_webapi_url, headers=pvout_Headers, data=pvout_Payload)

    if response.status_code == 200:
        return ("Data added successfully!")
    else:
        return(f"Error: {response.status_code}")






# This block is executed when the module is run directly
if __name__ == "__main__":
    # Test some examples
    print ("This is a library and cannot be ran standalone.")
