import re
import json
from netaddr import IPNetwork
from distutils import command
from netmiko import ConnectHandler

def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command(command)
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params, 'sh ip int br')
    result = data.strip().split('\n')
    for line in result[1:]:
        intf_type, intf_num, intf_ip = re.search(
            r'(\w)\w+(\d+/\d+)\s+(\d+.\d+.\d+.\d+|unassigned)', line).groups()
        if intf_type == intf[0] and intf_num == intf[1:]:
            return intf_ip

def get_subnet(device_params, intf):
  data = get_data_from_device(device_params, 'sh int ' + intf)
  try:
    cdiraddress = re.search(r'  Internet address is ([0-9./]+)', data).groups()
    return "%s"%IPNetwork(cdiraddress[0]).netmask
  except:
    return "unassigned"

def get_description(device_params, intf):
  data = get_data_from_device(device_params, 'sh int description')
  result = data.strip().split('\n')
  for line in result[1:]:
    line += ' '
    intf_type, intf_num, _, _, description = re.search(r'(\w)\w([0-9/]+)\s+(admin down|\w+)\s+(\w+)([0-9a-zA-Z\s/]+|null)', line).groups()
    if intf_type == intf[0] and intf_num == intf[1:]:
      return description.strip()

def get_status(device_params, intf):
  data = get_data_from_device(device_params, 'sh int description')
  result = data.strip().split('\n')
  for line in result[1:]:
    line += ' '
    intf_type, intf_num, status, _, _ = re.search(r'(\w)\w([0-9/]+)\s+(admin down|\w+)\s+(\w+)([0-9a-zA-Z\s/]+|null)', line).groups()
    if intf_type == intf[0] and intf_num == intf[1:]:
      return status

def get_neighbor_link(device_params, intf):
  data = get_data_from_device(device_params, 'sh cdp nei')
  result = data.strip().split('\n')
  for line in result[5:]:
    try:
      router_name, lo_intf_type, lo_intf_num, nei_intf_type, nei_intf_num = re.search(r'(\w+).\w+.\w+\s+(\w)\w+\s([0-9/]+)\s+\d+\s+.+?(?=Gig)(\w)\w+\s([0-9/]+)', line).groups()
      if lo_intf_type == intf[0] and lo_intf_num == intf[1:]:
        return "Connect to " + nei_intf_type + nei_intf_num + " of " + router_name
    except:
      return "Not Use"

def set_description(device_params, intf):
  commands = ["int " + intf, "description " + get_neighbor_link(device_params, intf)]
  with ConnectHandler(**device_params) as ssh:
    result = ssh.send_config_set(commands)
    print(result)
