import re
from netmiko import ConnectHandler
import json

device_ip = "172.31.107.4"
username = 'admin'
password = 'cisco'
device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}


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
    pass


def get_description(device_params, intf):
    data = get_data_from_device(device_params, 'sh int description')
    result = data.strip().split('\n')
    for line in result[1:]:
        # print(line)
        intf = re.search(r'\s\w+\s\w+', line)
        print(intf)


def set_description():
    jsonFile = open("testcase.json", "r")
    routersJson = json.load(jsonFile)
    jsonFile.close()

    for device in routersJson:
        with ConnectHandler(**device_params) as ssh:
            result = ssh.send_command('conf ter')

            result = ssh.send_command('conf ter')
