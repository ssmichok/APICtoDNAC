#!/usr/bin/env python
from urllib.request import Request, urlopen
import json
import ssl
import time
#
def myMain():
	DevSn = "FGL214891DD"
	myProjName = "PnProject"
	myTok = getToken()
	print("Getting Token: " + myTok)
	# devStat = getDevState(DevSn, myTok)
	# print("devStat: " + devStat)
	myListForDev = getDevBySn(DevSn, myTok)
	print("Getting Device ID: " + myListForDev[0])
	myTempId = getTempId(myProjName, myTok)
	print("Getting Template ID: " + myTempId)
	mySudi = SetDevSudi(myListForDev[0], DevSn, myTok)
	print("Setting SUDI...")
	myGoldenImageId = getGoldenImageId(myTok)
	print("Getting Golden Image Id...")
	myClaim = claimPnpDevice(myListForDev[0], myTempId, myGoldenImageId, myTok)
	# print ("myClaim: " + str(myClaim))
	if str(myClaim[1]) == "200":
		print(myClaim[0])
	else:
		print("Oooops...something went wrong... :-(")
		return('Not OK')
	i = 0
	while True:
		devStat = getDevState(DevSn, myTok)
		if devStat != "Provisioned":
			print ("Device Status: " + devStat)
			time.sleep(10)
			i = i + 1
			if i > 20:
				print("Can't provision this device :-(")
				break
		else:
			print ("Device Status: " + devStat)
			break

	return('OK')
#
#
def getToken():
    url = 'https://localhost:8443/api/system/v1/auth/token'
    values = {
	"username":"admin",
	"password":"P@ssw0rd"
    }
    data = json.dumps(values).encode('utf-8')
    req = Request(url, data)
    req.add_header('Authorization', 'Basic YWRtaW46UEBzc3cwcmQ=')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    gcontext = ssl.SSLContext()
    #
    response = urlopen(req, context=gcontext)
    response_string = response.read().decode('utf-8')
    # print(response_string)
    json_object = json.loads(response_string)
    # print(json.dumps(json_object, sort_keys=True, indent=4))
    myToken = json_object['Token']
    # print(myToken)
    response.close()
    return(myToken)
#
def SetDevSudi(myDevId, DevSn, myToken):
	url = 'https://localhost:8443/api/v1/onboarding/pnp-device/' + myDevId
	values_str = '{ "deviceInfo": { "userSudiSerialNos": [ "' + DevSn + '" ], "sudiRequired": "true" } }'
	values = json.loads(values_str)
	data = json.dumps(values).encode('utf-8')
	req = Request(url, data, method='PUT')
	req.add_header('X-Auth-Token', myToken)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Accept', 'application/json')
	gcontext = ssl.SSLContext()
	#
	response = urlopen(req, context=gcontext)
	response_string = response.read().decode('utf-8')
	json_object = json.loads(response_string)
	# print(json_object)
	response.close()
	return("SUDI set")

#
def claimPnpDevice(myDevId, myTempId, myGoldenImageId, myToken):
	url = 'https://localhost:8443/api/v1/onboarding/pnp-device/claim'
	values_str = '{ "pushDeviceIdCertificate": "true", "deviceClaimList": [ { "configList":[ { "configId":"' + myTempId + '", "configParameters":[ { "key": "logginHost", "value": "1.1.1.1"} ] }], "deviceId":"' + myDevId + '" } ], "configId":"' + myTempId + '", "imageId":"' + myGoldenImageId + '", "populateInventory":"false" }'
	values = json.loads(values_str)
	data = json.dumps(values).encode('utf-8')
	req = Request(url, data)
	req.add_header('X-Auth-Token', myToken)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Accept', 'application/json')
	gcontext = ssl.SSLContext()
	#
	response = urlopen(req, context=gcontext)
	response_string = response.read().decode('utf-8')
	# print(response_string)
	json_object = json.loads(response_string)
	# print(json.dumps(json_object, sort_keys=True, indent=4))
	myMessage = json_object['message']
	myStatusCode = json_object['statusCode']
	# print(myToken)
	response.close()
	return[myMessage, myStatusCode]

#
def getDevState(DevSn, myToken):
    url = 'https://localhost:8443/api/v1/onboarding/pnp-device?serialNumber=' + DevSn
    req = Request(url)
    req.add_header('X-Auth-Token', myToken)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    gcontext = ssl.SSLContext()
    #
    response = urlopen(req, context=gcontext)
    response_string = response.read().decode('utf-8')
    # print(response_string)
    json_object = json.loads(response_string)
    myDevInfo = json_object[0]['deviceInfo']
    # print (myDevInfo)
    for key, val in myDevInfo.items():
        # print('keys: ' + str(key) + ' vals: ' + str(val))
	    if str(key) == "state":
		    myState = str(val)
    response.close()
    return(str(myState))
#
def getTempId(myProjName, myToken):
	url = 'https://localhost:8443/dna/intent/api/v1/template-programmer/project?name=' + myProjName
	req = Request(url)
	req.add_header('X-Auth-Token', myToken)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Accept', 'application/json')
	gcontext = ssl.SSLContext()
	#
	response = urlopen(req, context=gcontext)
	response_string = response.read().decode('utf-8')
	json_object = json.loads(response_string)
	myTempList = json_object[0]['templates']
	for key, val in myTempList[0].items():
		# print('keys: ' + str(key) + ' vals: ' + str(val))
		if str(key) == "id":
			myTempId = str(val)
	response.close()
	return(myTempId)
#
def getGoldenImageId(myToken):
    url = 'https://localhost:8443/dna/intent/api/v1/image/importation?isTaggedGolden=true&family=C1100'
    req = Request(url)
    req.add_header('X-Auth-Token', myToken)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    gcontext = ssl.SSLContext()
    #
    response = urlopen(req, context=gcontext)
    response_string = response.read().decode('utf-8')
    json_object = json.loads(response_string)
    myImageList = json_object['response']
    for key, val in myImageList[0].items():
        # print('keys: ' + str(key) + ' vals: ' + str(val))
        if str(key) == "imageUuid":
            myImageId = str(val)
    response.close()
    return(myImageId)
#
def getDevBySn(DevSn, myToken):
	# url = 'https://localhost:8443/api/v1/onboarding/pnp-device?state=Unclaimed&serialNumber=' + DevSn
	url = 'https://localhost:8443/api/v1/onboarding/pnp-device?serialNumber=' + DevSn
	req = Request(url)
	req.add_header('X-Auth-Token', myToken)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Accept', 'application/json')
	gcontext = ssl.SSLContext()
    #
	response = urlopen(req, context=gcontext)
	response_string = response.read().decode('utf-8')
    # print(response_string)
	json_object = json.loads(response_string)
	myDevId = json_object[0]['id']
	myDevId = str(myDevId)
	myDevInfo = json_object[0]['deviceInfo']
	# print (myDevInfo)
	for key, val in myDevInfo.items():
        # print('keys: ' + str(key) + ' vals: ' + str(val))
	    if str(key) == "name":
		    myName = str(val)
	    if str(key) == "pid":
		    myPid = str(val)
	response.close()
	return [myDevId, myName, myPid]

if __name__ == "__main__":
	rtn = myMain()
