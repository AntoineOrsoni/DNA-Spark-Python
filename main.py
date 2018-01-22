"""
This script retrieves an authentication token from APIC-EM and prints out it's value
It is standalone, there is no dependency.
"""

import requests  # We use Python "requests" module to do HTTP GET query
import json  # Import JSON encoder and decode module

requests.packages.urllib3.disable_warnings()  # Disable warnings

# APIC-EM IP, modify these parameters if you are using your own APIC-EM
# apicem_ip = "devnetapi.cisco.com/sandbox/apic_em"
apicem_ip = "sandboxapic.cisco.com:443"
username = "devnetuser"
password = "Cisco123!"
version = "v1"
sparkToken = "ODVjODQ0ZDItZjI3ZC00ZTc5LWI2MTYtMzU3YWNhY2Y5ZDllMGUwMTIwODEtYTRj"
sparkRoomID = "Y2lzY29zcGFyazovL3VzL1JPT00vMTgyMDQxMDAtZTcwMS0xMWU3LTg4MjUtOTc2MWUwNDRiODJm"
deviceID = "d337811b-d371-444c-a49f-9e2791f955b4"
deviceIpAddress = "165.10.1.39"
botAccessToken = "OTI3NDAzMjctMWE5OS00NjViLWJkNWYtMjM1NWExZTdlZTU3OTY0NGI2NDQtZWE3"

# JSON
r_json = {
    "username": username,
    "password": password
}

# POST ticket API URL
post_url = "https://" + apicem_ip + "/api/" + version + "/ticket"

# GET url

# GET INTERFACES OF DEVICE-ID
# get_url = "https://"+apicem_ip+"/api/"+version+"/interface/network-device/"+deviceID

get_url = "https://" + apicem_ip + "/api/" + version + "/network-device/ip-address/" + deviceIpAddress
# get_url = "https://sandboxapic.cisco.com:443/api/v1/network-device/ip-address/165.10.1.39"

# All APIC-EM REST API request and response content type is JSON.
headers = {'content-type': 'application/json'}

# Make request and get response - "resp" is the response of this request
resp = requests.post(post_url, json.dumps(r_json), headers=headers, verify=False)
print ("Request Status: ", resp.status_code)

# Get the json-encoded content from response
response_json = resp.json()
print ("\nRaw response from POST ticket request:\n", resp.text)
# Not that easy to read the raw response, so try the formatted print out

# Pretty print the raw response
print ("\nPretty print response:\n", json.dumps(response_json, indent=4))

# ----------------------------------------
# Spark work
# ----------------------------------------


# serviceTicket = service ticket returned by the APIC
serviceTicket = response_json["response"]["serviceTicket"]
print("\n \n Service ticket = " + serviceTicket)

# ----------------------------------------
# Get device state
# ----------------------------------------

# Example of deviceID : d337811b-d371-444c-a49f-9e2791f955b4

get_headers = {
    "X-Auth-Token": serviceTicket,
    "Cache-Control": "no-cache",
    'Postman-Token': "61b3cbf7-ef6a-cbc8-d66b-b55b31d2c453"
}

get_params = {"ipAddress": deviceIpAddress}

getDeviceInfo = requests.request("GET", get_url, headers=get_headers)


print("\n \n Response code " + str(getDeviceInfo.status_code))

print("\n \n" + "Device information : " + "\n", json.dumps(getDeviceInfo.json(), indent=4))

print("\n \n")
# JSON : build the message

deviceStatus = getDeviceInfo.json()["response"]['reachabilityStatus']

sparkMessage = "The device " + deviceIpAddress + " is " + deviceStatus

spark_json = {
    "roomId": sparkRoomID,
    "text": sparkMessage
}

# POST the message on the room
spark_post_url = "https://api.ciscospark.com/v1/messages"
spark_headers = {
    "Authorization": "Bearer " + sparkToken,
    "Content-Type": "application/json"
}

spark_resp = requests.post(spark_post_url, json.dumps(spark_json), headers=spark_headers, verify=False)
print("Spark status ", spark_resp.status_code)

spark_response_json = spark_resp.json()
print("Pretty response from Spark :", json.dumps(spark_response_json, indent=4))
