import json
from urllib.request import urlopen

def getCountry(ipaddress):
    response = urlopen("https://ipstack.com/ipstack_api.php?ip="+ipaddress).read().decode('utf-8')
    responseJson = json.loads(response)
    #print(responseJson)
    return responseJson.get("country_name")

country = getCountry("50.78.253.48")
print(country)
