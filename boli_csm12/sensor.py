"""Sensor platform for Boli CSM12 Modbus Electric Meter."""
from __future__ import annotations

import logging
import struct

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

# 名称映射表，兜底用
SENSOR_NAMES = {
    "en": {
        "voltage": "Voltage",
        "current": "Current",
        "active_power": "Active Power",
        "apparent_power": "Apparent Power",
        "reactive_power": "Reactive Power",
        "power_factor": "Power Factor",
        "phase_angle": "Phase Angle",
        "frequency": "Frequency",
        "import_active_energy": "Import Active Energy",
        "export_active_energy": "Export Active Energy",
        "import_reactive_energy": "Import Reactive Energy",
        "export_reactive_energy": "Export Reactive Energy",
        "total_reactive_energy": "Total Reactive Energy",
        "carbon_emission": "Carbon Emission",
        "power_demand": "Power Demand",
        "active_energy": "Total Active Energy",
    },
    "zh-Hans": {
        "voltage": "电压",
        "current": "电流",
        "active_power": "有功功率",
        "apparent_power": "视在功率",
        "reactive_power": "无功功率",
        "power_factor": "功率因数",
        "phase_angle": "相位角",
        "frequency": "频率",
        "import_active_energy": "正向有功电能",
        "export_active_energy": "反向有功电能",
        "import_reactive_energy": "正向无功电能",
        "export_reactive_energy": "反向无功电能",
        "total_reactive_energy": "总无功电能",
        "carbon_emission": "碳排放",
        "power_demand": "功率需量",
        "active_energy": "累计有功电能",
    }
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Boli CSM12 sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    device_info = data["device_info"]

    entities = []
    for description in SENSOR_TYPES:
        entities.append(
            BoliCSM12Sensor(
                hass=hass,
                coordinator=coordinator,
                description=description,
                device_info=device_info,
                unique_id=f"{entry.entry_id}_{description.key}",
            )
        )

    async_add_entities(entities, True)


class BoliCSM12Sensor(CoordinatorEntity, SensorEntity):
    """Boli CSM12 sensor with fallback name localization."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        description,
        device_info: dict,
        unique_id: str,
    ) -> None:
        super().__init__(coordinator)
        self.hass = hass
        self.entity_description = description
        self._attr_translation_key = description.translation_key
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info

        self._key = description.key
        self._scale = description.scale
        self._precision = description.precision
        self._data_type = description.data_type

    @property
    def name(self):
        """Dynamic name based on user language, fallback for translation_key."""
        lang = self.hass.config.language
        return SENSOR_NAMES.get(lang, SENSOR_NAMES["en"]).get(self._key, self._key)

    @property
    def native_value(self):
        """Calculate sensor value from raw register data."""
        raw_regs = self.coordinator.data.get(self._key)
        if not raw_regs or len(raw_regs) < 2:
            return None

        if self._data_type == "float32":
            raw_bytes = struct.pack(">HH", raw_regs[0], raw_regs[1])
            value = struct.unpack(">f", raw_bytes)[0]
        else:
            value = raw_regs[0]

        return round(value * self._scale, self._precision)