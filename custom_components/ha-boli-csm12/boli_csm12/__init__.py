"""Boli CSM12 Modbus Electric Meter integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_TYPES
from .modbus_rtu import ModbusRtuClient

_LOGGER = logging.getLogger(__name__)

# Global serial port connection pool
modbus_clients: Dict[str, ModbusRtuClient] = {}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Boli CSM12 from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    port = entry.data["port"]
    baudrate = entry.data["baudrate"]
    bytesize = entry.data.get("bytesize", 8)
    parity = entry.data["parity"]
    stopbits = entry.data["stopbits"]
    timeout = entry.data["timeout"]
    slave = entry.data["slave"]

    if port not in modbus_clients:
        try:
            client = await hass.async_add_executor_job(
                ModbusRtuClient,
                port,
                baudrate,
                bytesize,
                parity,
                stopbits,
                timeout,
            )
        except Exception as ex:
            _LOGGER.error("Failed to open serial port %s: %s", port, str(ex))
            return False

        modbus_clients[port] = client
        _LOGGER.info("Modbus serial connection created: %s", port)

    client = modbus_clients[port]
    device_info = {
        "identifiers": {(DOMAIN, f"{port}_{slave}")},
        "name": f"Boli CSM12 (Port: {port.split('/')[-1]}, Slave: {slave})",
        "manufacturer": "Boli Electronics",
        "model": "CSM12",
        "sw_version": "1.0",
    }

    async def async_update_data():
        """Read all registers in fixed order."""
        try:
            data = {}
            for desc in SENSOR_TYPES:
                count = 2 if desc.data_type == "float32" else 1
                if desc.input_type == "input":
                    regs = await hass.async_add_executor_job(
                        client.read_input_registers, slave, desc.address, count
                    )
                else:
                    regs = await hass.async_add_executor_job(
                        client.read_holding_registers, slave, desc.address, count
                    )
                data[desc.key] = regs
            return data

        except Exception as ex:
            raise UpdateFailed(f"Read failed: {ex}") from ex

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"Boli CSM12 Slave {slave}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "slave": slave,
        "port": port,
        "device_info": device_info,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, ["sensor"]):
        port = hass.data[DOMAIN][entry.entry_id]["port"]
        hass.data[DOMAIN].pop(entry.entry_id)

        has_other_users = any(
            data["port"] == port for data in hass.data[DOMAIN].values()
        )

        if not has_other_users and port in modbus_clients:
            modbus_clients[port].close()
            modbus_clients.pop(port)
            _LOGGER.info("Modbus serial connection closed: %s", port)

    return unload_ok