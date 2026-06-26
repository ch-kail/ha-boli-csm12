# Boli CSM12 Electric Meter | 博立 CSM12 电能表

Home Assistant custom integration for Boli CSM12 series Modbus RTU electric meters.
博立 CSM12 系列 Modbus RTU 电能表 Home Assistant 自定义集成。

## Features | 功能特性
- 100% UI configuration, no YAML editing required
- 全图形化配置，无需修改任何配置文件
- Support multi meters share one serial port
- 支持多台电表共用同一个串口
- Built-in 16 measurement parameters: voltage, current, power, energy, frequency, etc.
- 内置16项测量参数：电压、电流、功率、电能、频率等
- Auto serial port detection, connection test
- 自动识别串口，自带通信测试功能
- Support Chinese and English UI
- 支持中英文双语言界面

## Hardware Wiring | 硬件接线
| Meter RS485 | USB-RS485 Adapter |
|------------|-------------------|
| A          | A / D+ / T/R+    |
| B          | B / D- / T/R-    |
| GND        | GND (optional)   |

## Installation | 安装方法
### Method 1: HACS (Recommended)
1. Open HACS → Integrations → ⋮ → Custom repositories
2. Paste this repository URL, select category **Integration**
3. Search "Boli CSM12" and install
4. Restart Home Assistant

### Method 2: Manual Install
1. Download the latest release
2. Copy `custom_components/boli_csm12` folder to your HA `config/custom_components/` directory
3. Restart Home Assistant

## Setup | 配置步骤
1. Go to **Settings → Devices & Services → Add Integration**
2. Search **Boli CSM12 Electric Meter**
3. Select your serial port, set baud rate (default 9600), parity (Even), stop bits (1)
4. Enter slave address of your meter (default 21)
5. Submit and all sensors will be created automatically

## FAQ | 常见问题
**Q: Serial permission error?**
A: Run command: `sudo usermod -aG dialout homeassistant` then reboot.

**Q: No data / communication timeout?**
A: Check A/B wiring, confirm slave address and baud rate match meter settings.
