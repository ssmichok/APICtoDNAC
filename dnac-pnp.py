#!/usr/bin/env python
from urllib.request import Request, urlopen
import json
import ssl
#
def myMain():
	myTok = getToken()
	# print("Token: " + myTok)
	devStat = getDevState(myTok)
	print("devStat: " + devStat)
    return ('OK')

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
def getDevState(myToken):
    url = 'https://localhost:8443/api/v1/onboarding/pnp-device?serialNumber=FGL214891DD'
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
	    if str(key) == "onbState":
		    myState = str(val)
    response.close()
    return(str(myState))


if __name__ == "__main__":
	rtn = myMain()
