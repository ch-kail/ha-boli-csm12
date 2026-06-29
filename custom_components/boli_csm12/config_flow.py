"""Config flow for Boli CSM12 Modbus Electric Meter integration."""
from __future__ import annotations

import serial.tools.list_ports
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    DEFAULT_SLAVE,
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
    BAUDRATE_OPTIONS,
    PARITY_OPTIONS,
    STOPBITS_OPTIONS,
)
from .modbus_rtu import ModbusRtuClient


class BoliCSM12ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Boli CSM12."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            test_success, error_key = await self._test_modbus_connection(user_input)
            if test_success:
                return self.async_create_entry(
                    title=f"Boli CSM12 ({user_input['port'].split('/')[-1]}, Slave {user_input['slave']})",
                    data=user_input,
                )
            errors["base"] = error_key

        ports = await self.hass.async_add_executor_job(self._get_available_ports)
        default_port = ports[0] if ports else ""

        data_schema = vol.Schema({
            vol.Required("port", default=default_port): vol.In(ports),
            vol.Required("baudrate", default=DEFAULT_BAUDRATE): vol.In(BAUDRATE_OPTIONS),
            vol.Required("parity", default=DEFAULT_PARITY): vol.In(PARITY_OPTIONS),
            vol.Required("stopbits", default=DEFAULT_STOPBITS): vol.In(STOPBITS_OPTIONS),
            vol.Required("slave", default=DEFAULT_SLAVE): int,
            vol.Optional("timeout", default=DEFAULT_TIMEOUT): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    def _get_available_ports() -> list[str]:
        """Scan available serial ports."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if not ports:
            ports.append("no_port_found")
        return ports

    async def _test_modbus_connection(self, config: dict) -> tuple[bool, str]:
        """Test Modbus connection, return error key."""
        client = None
        try:
            client = await self.hass.async_add_executor_job(
                ModbusRtuClient,
                config["port"],
                config["baudrate"],
                DEFAULT_BYTESIZE,
                config["parity"],
                config["stopbits"],
                config["timeout"],
            )

            await self.hass.async_add_executor_job(
                client.read_input_registers,
                config["slave"],
                0x0000,
                2,
            )

            return True, ""

        except Exception as ex:
            if "Permission denied" in str(ex):
                return False, "permission_denied"
            if "timeout" in str(ex).lower() or "超时" in str(ex):
                return False, "communication_timeout"
            if "CRC" in str(ex):
                return False, "crc_error"
            return False, "connection_failed"
        finally:
            if client:
                client.close()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        super().__init__()
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=user_input
            )
            await self.hass.config_entries.async_reload(self._config_entry.entry_id)
            return self.async_create_entry(title="", data=user_input)

        data = self._config_entry.data
        data_schema = vol.Schema({
            vol.Required("port", default=data["port"]): str,
            vol.Required("baudrate", default=data["baudrate"]): vol.In(BAUDRATE_OPTIONS),
            vol.Required("parity", default=data["parity"]): vol.In(PARITY_OPTIONS),
            vol.Required("stopbits", default=data["stopbits"]): vol.In(STOPBITS_OPTIONS),
            vol.Required("slave", default=data["slave"]): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )