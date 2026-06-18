"""广东博立科技CSM12电能表传感器定义"""
import logging
import struct
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pymodbus.client import ModbusSerialClient
from .const import *

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """根据配置条目创建传感器"""
    coordinator = BoliCSM12Coordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_def in SENSOR_DEFINITIONS:
        entities.append(BoliCSM12Sensor(coordinator, sensor_def, entry))

    async_add_entities(entities, True)

class BoliCSM12Coordinator(DataUpdateCoordinator):
    """Modbus数据更新协调器"""
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.entry = entry
        self.config = entry.data
        self.client = ModbusSerialClient(
            port=self.config["port"],
            baudrate=self.config["baudrate"],
            parity=self.config["parity"],
            stopbits=self.config["stopbits"],
            bytesize=8,
            method="rtu",
            timeout=DEFAULT_TIMEOUT,
        )

    async def _async_update_data(self):
        """从电能表读取所有数据"""
        try:
            data = {}
            for sensor_def in SENSOR_DEFINITIONS:
                value = await self.hass.async_add_executor_job(
                    self._read_register, sensor_def
                )
                data[sensor_def["key"]] = value
            return data
        except Exception as e:
            raise UpdateFailed(f"读取电能表数据失败: {str(e)}") from e

    def _read_register(self, sensor_def):
        """读取单个寄存器并解析"""
        address = sensor_def["address"]
        data_type = sensor_def["data_type"]
        scale = sensor_def["scale"]
        slave = self.config["slave"]

        count = 2 if data_type == "float32" else 1
        response = self.client.read_input_registers(address, count, slave=slave)
        
        if response.isError():
            raise Exception(f"寄存器0x{address:04X}读取失败")

        if data_type == "float32":
            # 大端序解析32位浮点数（大多数电能表使用大端序）
            raw = struct.pack('>HH', response.registers[0], response.registers[1])
            return round(struct.unpack('>f', raw)[0] * scale, sensor_def["precision"])
        else:
            return round(response.registers[0] * scale, sensor_def["precision"])

class BoliCSM12Sensor(SensorEntity):
    """电能表传感器实体"""
    def __init__(self, coordinator, sensor_def, entry):
        self.coordinator = coordinator
        self.sensor_def = sensor_def
        self.entry = entry
        
        self._attr_unique_id = f"{entry.entry_id}_{sensor_def['key']}"
        self._attr_name = sensor_def["name"]
        self._attr_unit_of_measurement = sensor_def["unit_of_measurement"]
        self._attr_device_class = sensor_def["device_class"]
        self._attr_state_class = sensor_def["state_class"]
        self._attr_precision = sensor_def["precision"]
        self._attr_icon = sensor_def["icon"]
        self._attr_should_poll = False

    @property
    def device_info(self):
        """设备信息，所有传感器自动关联到同一个设备"""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.title,
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "sw_version": VERSION,
        }

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def state(self):
        return self.coordinator.data.get(self.sensor_def["key"])

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )