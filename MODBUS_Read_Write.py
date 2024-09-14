# pip install pymodbustcp
# Documentation: https://pymodbustcp.readthedocs.io/en/latest/

from pyModbusTCP.client import ModbusClient
myModbusClient = ModbusClient(host="192.168.0.3", port=510)
address = 1
numerOfValues = 1
parameterPayload = 15

response = myModbusClient.read_holding_registers(address, numerOfValues)
print("[*] Response from PLC, address: ", address, " has value: ", response[0])
myModbusClient.write_single_register(address, parameterPayload)
print("[*] Writing: ", parameterPayload, " to address: ",address)
