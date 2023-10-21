
# Copyright (C) 2023 Alessio Rossini <alessior@live.com>
# Original source code available at https://github.com/AxReds/PVOut.org
#



# Purpose: Micropython Code to turn a Raspberry Pico into a controller for fireworks ignition
# File Name: controller-main.py *****REMEMBER TO RENAME IT TO JUST main.py BEFORE UPLOADING THE FILE TO THE PICO *****
# Author: Alessio Rossini <alessior@live.com>
# Description:
#         This code for will controll a Raspberry-based system to remotely ignite fireworks using wireless communication.
#         The system consists of two Raspberries:
#         - the first one serving as a transmitter and will controll the sequence of ignition
#         - the second one will act as a receiver and will controll the current to ignite the fuses. 
#  
#         The controller allows the user to send commands to the receiver to ignite one of four fireworks by entering a number between 1 and 4 on the serial monitor.
#          The receiver listens for incoming commands, ignites the corresponding firework, and sends a confirmation message back to the transmitter.
#
#  Original Idea and Source Code:
#         The original source code was written by @overVolt (https://github.com/overVolt)
#         and is available at https://pastebin.com/u/overVoltOfficial.
#



# License:
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software Foundation;
# either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details
# https://opensource.org/
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
#
#
###############################################################################
#
#Library Declaration
#Built-in Libraries
import json

#Third Party Libraries

#Custom Libraries
from pvoutput import *


#
# Read information from the JSON file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

#
# Access PVOutput information in the JSON file to set constants values
PVOutputConfig = config_data['PVOutput']
import_file = PVOutputConfig['InputFile']
Apikey = PVOutputConfig['ApiKey']
SystemId = PVOutputConfig['SystemId']

# Open the text file in read mode
with open(import_file, "r") as f:
    # Read the lines of the file
    lines = f.readlines()

# Create an empty list to store the data to send
#data = []

# For each line of the file
i = 0
for line in lines:
    # Remove whitespace and split the line by commas
    line = line.strip().split(",")
    i=i+1

    # Create a dictionary with keys corresponding to the parameters of the update status API
    record_payload = {
        "d": line[0], # Date
        "t": line[1],
        "v1": line[2], # Energy generated
        "v2": line[3], # Energy consumed
        # Add any other optional parameters
    }

    #Append and print the result
    print(PVOut_AddStatusService(Apikey,SystemId,record_payload),", Added Record No.:", i)
