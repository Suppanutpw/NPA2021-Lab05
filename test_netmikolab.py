import json
from netmikolab import *

username = 'admin'
password = 'cisco'
device_params = [
  {
    'device_type': 'cisco_ios',
    'ip': "172.31.107.4",
    'username': username,
    'password': password
  },
  {
    'device_type': 'cisco_ios',
    'ip': "172.31.107.5",
    'username': username,
    'password': password
  },
  {
    'device_type': 'cisco_ios',
    'ip': "172.31.107.6",
    'username': username,
    'password': password
  }
]

jsonFile = open("testcase.json", "r")
routersJson = json.load(jsonFile)
jsonFile.close()

# routerJson[0]['Interfaces'][0] // R1 G0/0
# routerJson[0]['Interfaces'][1] // R1 G0/1

def test_ip():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_ip(device_params[index], interface["Interface"]) == interface["IP"]
      index += 1

def test_subnet():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_subnet(device_params[index], interface["Interface"]) == interface["Subnet"]
      index += 1

def test_description():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_description(device_params[index], interface["Interface"]) == interface["Description"]
      index += 1
