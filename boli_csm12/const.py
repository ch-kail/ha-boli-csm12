"""广东博立科技CSM12电能表常量定义"""

DOMAIN = "boli_csm12"
NAME = "广东博立科技 CSM12电能表"
MANUFACTURER = "广东博立科技"
MODEL = "CSM12"
VERSION = "1.0.0"

# 默认Modbus通信参数（可在UI中修改）
DEFAULT_BAUDRATE = 9600
DEFAULT_PARITY = "E"
DEFAULT_STOPBITS = 1
DEFAULT_SLAVE = 21
DEFAULT_TIMEOUT = 3
DEFAULT_SCAN_INTERVAL = 10  # 数据更新间隔（秒）

# CSM12电能表完整寄存器定义
# 请根据你的产品手册确认所有地址和参数
SENSOR_DEFINITIONS = [
    {
        "key": "voltage",
        "name": "电压",
        "address": 0x0000,
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "V",
        "scale": 0.1,
        "precision": 1,
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:flash",
    },
    {
        "key": "current",
        "name": "电流",
        "address": 0x0006,
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "A",
        "scale": 0.001,
        "precision": 3,
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    {
        "key": "active_power",
        "name": "有功功率",
        "address": 0x000c,
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "kW",
        "scale": 1,
        "precision": 4,
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt",
    },
    {
        "key": "reactive_power",
        "name": "无功功率",
        "address": 0x0012,  # 请替换为实际地址
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "kvar",
        "scale": 1,
        "precision": 4,
        "device_class": "reactive_power",
        "state_class": "measurement",
        "icon": "mdi:lightning-bolt-outline",
    },
    {
        "key": "power_factor",
        "name": "功率因数",
        "address": 0x0018,  # 请替换为实际地址
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "",
        "scale": 0.001,
        "precision": 3,
        "device_class": "power_factor",
        "state_class": "measurement",
        "icon": "mdi:angle-acute",
    },
    {
        "key": "frequency",
        "name": "电网频率",
        "address": 0x001E,  # 请替换为实际地址
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "Hz",
        "scale": 0.01,
        "precision": 2,
        "device_class": "frequency",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    {
        "key": "active_energy",
        "name": "累计有功电能",
        "address": 0x0156,
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "kWh",
        "scale": 0.01,
        "precision": 2,
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt-circle",
    },
    {
        "key": "reactive_energy",
        "name": "累计无功电能",
        "address": 0x015A,  # 请替换为实际地址
        "input_type": "input",
        "data_type": "float32",
        "unit_of_measurement": "kvarh",
        "scale": 0.01,
        "precision": 2,
        "device_class": "energy",
        "state_class": "total_increasing",
        "icon": "mdi:lightning-bolt-circle-outline",
    },
]