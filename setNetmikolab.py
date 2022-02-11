import re
import json
import netmiko


def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command(command)
        return result_shipintbr


def get_neighbor_link(device_params, intf):
    data = get_data_from_device(device_params, 'sh cdp nei')
    result = data.strip().split('\n')
    for line in result[5:]:
        try:
            router_name, lo_intf_type, lo_intf_num, nei_intf_type, nei_intf_num = re.search(
                r'(\w+).\w+.\w+\s+(\w)\w+\s([0-9/]+)\s+\d+\s+.+?(?=Gig)(\w)\w+\s([0-9/]+)', line).groups()
            if lo_intf_type == intf[0] and lo_intf_num == intf[1:]:
                return "Connect to " + nei_intf_type + nei_intf_num + " of " + router_name
        except:
            return "Not Use"


def set_description(device_params, intf):
    commands = ["int " + intf, "description " +
                get_neighbor_link(device_params, intf)]
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_config_set(commands)
        print(result)


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

for device_param in device_params:
    for interface in ["G0/0", "G0/1", "G0/2", "G0/3"]:
        set_description(device_param, interface)