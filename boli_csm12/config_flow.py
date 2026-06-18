"""广东博立科技CSM12电能表UI配置流程"""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from .const import *

class BoliCSM12ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            unique_id = f"boli_csm12_{user_input['port']}_{user_input['slave']}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"CSM12电能表(从站{user_input['slave']})",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self._build_schema(),
            errors=errors
        )

    def _build_schema(self):
        """自动扫描系统所有串口设备"""
        try:
            import serial.tools.list_ports
            ports = [port.device for port in serial.tools.list_ports.comports()]
        except Exception:
            ports = []
        
        # 添加常见串口作为备选
        common_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0", "/dev/ttyAMA0"]
        for port in common_ports:
            if port not in ports:
                ports.append(port)

        return vol.Schema({
            vol.Required("port", default=ports[0] if ports else "/dev/ttyUSB0"): vol.In(ports),
            vol.Required("slave", default=DEFAULT_SLAVE): vol.All(vol.Coerce(int), vol.Range(min=1, max=247)),
            vol.Required("baudrate", default=DEFAULT_BAUDRATE): vol.In([9600, 19200, 38400, 115200]),
            vol.Required("parity", default=DEFAULT_PARITY): vol.In({"N": "无校验", "E": "偶校验", "O": "奇校验"}),
            vol.Required("stopbits", default=DEFAULT_STOPBITS): vol.In([1, 2]),
        })