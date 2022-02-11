import json
import pytest
from netmikolabfinal import *

jsonFile = open("testcase.json", "r")
routersJson = json.load(jsonFile)
jsonFile.close()

device_params = []
for routerJson in routersJson:
  device_params.append(
    {
      'device_type': routerJson["Device_type"],
      'ip': routerJson["IP"],
      'username': routerJson["Username"],
      'password': routerJson["Password"]
    }
  )

@pytest.mark.ip
def test_ip():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_ip(device_params[index], interface["Interface"]) == interface["IP"], \
          device["Hostname"] + " - " + interface["Interface"] + " fail"
      index += 1

@pytest.mark.subnet
def test_subnet():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_subnet(device_params[index], interface["Interface"]) == interface["Subnet"], \
          device["Hostname"] + " - " + interface["Interface"] + " fail"
      index += 1

@pytest.mark.description
def test_description():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_description(device_params[index], interface["Interface"]) == interface["Description"]
      index += 1

@pytest.mark.status
def test_status():
    index = 0
    for device in routersJson:
      for interface in device['Interfaces']:
        assert get_interface_status(device_params[index], interface["Interface"]) == interface["Status"]
      index += 1
