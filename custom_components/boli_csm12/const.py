"""Constants for Boli CSM12 Modbus Electric Meter integration."""
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.const import (
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfPower,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfApparentPower,
    UnitOfReactivePower,
)

DOMAIN = "boli_csm12"
NAME = "Boli CSM12 Electric Meter"
VERSION = "2.1.1"

# Default Modbus parameters
DEFAULT_BAUDRATE = 9600
DEFAULT_BYTESIZE = 8
DEFAULT_PARITY = "E"
DEFAULT_STOPBITS = 1
DEFAULT_TIMEOUT = 3
DEFAULT_DELAY = 0.5
DEFAULT_SLAVE = 21

# UI dropdown options
BAUDRATE_OPTIONS = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
PARITY_OPTIONS = {"N": "None", "O": "Odd", "E": "Even"}
STOPBITS_OPTIONS = [1, 1.5, 2]


@dataclass(frozen=True)
class ModbusSensorEntityDescription(SensorEntityDescription):
    """Extended sensor description with Modbus fields."""
    address: int = 0
    input_type: str = "input"
    data_type: str = "uint16"
    scale: float = 1.0
    precision: int = 0


# Full register definitions with translation keys
SENSOR_TYPES: tuple[ModbusSensorEntityDescription, ...] = (
    # Voltage 30001 → 0x0000
    ModbusSensorEntityDescription(
        key="voltage",
        translation_key="voltage",
        address=0x0000,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        scale=0.1,
        precision=1,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Current 30007 → 0x0006
    ModbusSensorEntityDescription(
        key="current",
        translation_key="current",
        address=0x0006,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        scale=0.001,
        precision=3,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Active power 30013 → 0x000C
    ModbusSensorEntityDescription(
        key="active_power",
        translation_key="active_power",
        address=0x000C,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        scale=0.0001,
        precision=4,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Apparent power 30019 → 0x0012
    ModbusSensorEntityDescription(
        key="apparent_power",
        translation_key="apparent_power",
        address=0x0012,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kVA",
        scale=0.0001,
        precision=4,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Reactive power 30025 → 0x0018
    ModbusSensorEntityDescription(
        key="reactive_power",
        translation_key="reactive_power",
        address=0x0018,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kVAR",
        scale=0.0001,
        precision=4,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Power factor 30031 → 0x001E
    ModbusSensorEntityDescription(
        key="power_factor",
        translation_key="power_factor",
        address=0x001E,
        input_type="input",
        data_type="float32",
        scale=0.001,
        precision=3,
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Frequency 30071 → 0x0046
    ModbusSensorEntityDescription(
        key="frequency",
        translation_key="frequency",
        address=0x0046,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        scale=0.01,
        precision=2,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Import active energy 30073 → 0x0048
    ModbusSensorEntityDescription(
        key="import_active_energy",
        translation_key="import_active_energy",
        address=0x0048,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        scale=0.01,
        precision=2,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Export active energy 30075 → 0x004A
    ModbusSensorEntityDescription(
        key="export_active_energy",
        translation_key="export_active_energy",
        address=0x004A,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        scale=0.01,
        precision=2,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Import reactive energy 30077 → 0x004C
    ModbusSensorEntityDescription(
        key="import_reactive_energy",
        translation_key="import_reactive_energy",
        address=0x004C,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kvarh",
        scale=0.01,
        precision=2,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Export reactive energy 30079 → 0x004E
    ModbusSensorEntityDescription(
        key="export_reactive_energy",
        translation_key="export_reactive_energy",
        address=0x004E,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kvarh",
        scale=0.01,
        precision=2,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Total reactive energy 30081 → 0x0050
    ModbusSensorEntityDescription(
        key="total_reactive_energy",
        translation_key="total_reactive_energy",
        address=0x0050,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kvarh",
        scale=0.01,
        precision=2,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Carbon emission 30083 → 0x0052
    ModbusSensorEntityDescription(
        key="carbon_emission",
        translation_key="carbon_emission",
        address=0x0052,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement="kg CO₂",
        scale=0.01,
        precision=2,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Power demand 30085 → 0x0054
    ModbusSensorEntityDescription(
        key="power_demand",
        translation_key="power_demand",
        address=0x0054,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        scale=0.0001,
        precision=4,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Total active energy 30343 → 0x0156
    ModbusSensorEntityDescription(
        key="active_energy",
        translation_key="active_energy",
        address=0x0156,
        input_type="input",
        data_type="float32",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        scale=0.01,
        precision=2,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)
