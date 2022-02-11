import re
import json
import textfsm
from netaddr import IPNetwork
from netmiko import ConnectHandler

def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command(command)
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params, 'sh ip int br')
    with open("cisco_ios_show_ip_interface_brief.textfsm") as template:
        fsm = textfsm.TextFSM(template)
        interfaces = fsm.ParseText(data)
        for interface in interfaces:
            intf_type, intf_num = re.search(r'(\w)\w+(\d+/\d+|\d+)', interface[0]).groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return interface[1]

def get_subnet(device_params, intf):
    data = get_data_from_device(device_params, 'sh int ' + intf)
    with open("cisco_ios_show_interfaces.textfsm") as template:
        fsm = textfsm.TextFSM(template)
        interfaces = fsm.ParseText(data)
        return "%s"%IPNetwork(interfaces[0][7]).netmask

def get_description(device_params, intf):
    data = get_data_from_device(device_params, 'sh int description')
    with open("cisco_ios_show_interfaces_description.textfsm") as template:
        fsm = textfsm.TextFSM(template)
        interfaces = fsm.ParseText(data)
        for interface in interfaces:
            intf_type, intf_num = re.search(r'(\w)\w+(\d+/\d+|\d+)', interface[0]).groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return interface[3]

def get_interface_status(device_params, intf):
    data = get_data_from_device(device_params, 'sh int description')
    with open("cisco_ios_show_interfaces_description.textfsm") as template:
        fsm = textfsm.TextFSM(template)
        interfaces = fsm.ParseText(data)
        for interface in interfaces:
            intf_type, intf_num = re.search(r'(\w)\w+(\d+/\d+|\d+)', interface[0]).groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return interface[1]


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
