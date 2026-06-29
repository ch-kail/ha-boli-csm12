"""轻量 Modbus RTU 原生实现，兼容所有环境。"""
from __future__ import annotations

import struct
import time
import serial
import threading


def _crc16(data: bytes) -> int:
    """计算 Modbus RTU CRC16 校验码。"""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


class ModbusRtuClient:
    """线程安全的 Modbus RTU 串口客户端。"""

    def __init__(
        self,
        port: str,
        baudrate: int,
        bytesize: int = 8,
        parity: str = "E",
        stopbits: int = 1,
        timeout: float = 3.0,
        inter_frame_delay: float = 0.1,
    ) -> None:
        self._lock = threading.Lock()
        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
        )
        # 计算每字符位数
        bits_per_char = 1 + bytesize + (1 if parity != "N" else 0) + stopbits
        # 3.5 字符标准帧间隔，保底 50ms
        self._frame_delay = max((3.5 * bits_per_char) / baudrate, 0.05)
        # 请求间额外处理延迟，兼容低速电表
        self._inter_frame_delay = inter_frame_delay
        self._last_send_time = 0.0

    def close(self) -> None:
        """关闭串口连接。"""
        with self._lock:
            if self._serial.is_open:
                self._serial.close()

    def read_input_registers(self, slave: int, address: int, count: int) -> list[int]:
        """读取输入寄存器（功能码 0x04）。"""
        return self._read_registers(slave, 0x04, address, count)

    def read_holding_registers(self, slave: int, address: int, count: int) -> list[int]:
        """读取保持寄存器（功能码 0x03）。"""
        return self._read_registers(slave, 0x03, address, count)

    def _read_registers(self, slave: int, func_code: int, address: int, count: int) -> list[int]:
        """组装请求帧，分阶段读取响应，兼容低速设备。"""
        req = struct.pack(">BBHH", slave, func_code, address, count)
        req += struct.pack("<H", _crc16(req))

        with self._lock:
            # 请求间总延迟 = 标准帧间隔 + 设备处理延迟
            min_interval = self._frame_delay + self._inter_frame_delay
            elapsed = time.time() - self._last_send_time
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            # 清空接收缓冲区后发送请求
            self._serial.reset_input_buffer()
            self._serial.write(req)
            self._serial.flush()
            self._last_send_time = time.time()

            # 第一步：读取 3 字节响应头（从站地址 + 功能码 + 字节数）
            header = self._serial.read(3)
            if len(header) < 3:
                raise ConnectionError("Modbus 响应超时：未收到完整响应头")

            resp_slave, resp_func, byte_count = struct.unpack(">BBB", header)

            # 异常响应处理
            if resp_func & 0x80:
                err_code = self._serial.read(1)
                if len(err_code) == 1:
                    raise ConnectionError(f"Modbus 异常响应：异常码 {err_code[0]:02X}")
                raise ConnectionError("Modbus 响应异常：格式错误")

            # 第二步：读取剩余数据 + CRC
            remain_len = byte_count + 2
            data = self._serial.read(remain_len)
            if len(data) < remain_len:
                raise ConnectionError("Modbus 响应超时：数据帧不完整")

        # CRC 校验
        resp_body = header + data[:byte_count]
        expected_crc = _crc16(resp_body)
        actual_crc = struct.unpack("<H", data[byte_count:byte_count+2])[0]
        if expected_crc != actual_crc:
            raise ConnectionError(f"Modbus CRC 校验失败：预期 {expected_crc:04X}，实际 {actual_crc:04X}")

        # 解析寄存器（大端序）
        registers = []
        for i in range(0, byte_count, 2):
            registers.append(struct.unpack(">H", data[i:i+2])[0])

        return registers