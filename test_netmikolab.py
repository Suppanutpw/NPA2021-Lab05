from netmikolab import *

device_ip = "172.31.107.4"
username = 'admin'
password = 'cisco'
device_params = {
  'device_type': 'cisco_ios',
  'ip': device_ip,
  'username': username,
  'password': password
}

def test_ip():
  assert get_ip(device_params, "GO/0") == "172.31.112.4"
  assert get_ip(device_params, "G0/1") == "172.31.112.17"
  assert get_ip(device_params, "G0/2") == "172.31.112.33"
  assert get_ip(device_params, "G0/3") == "unassigned"
