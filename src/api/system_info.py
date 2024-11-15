from typing import Dict
import psutil


class SystemInfoAPI:
    def get_system_info(self):
            cpu_freq = psutil.cpu_freq().current
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_info = psutil.virtual_memory()
            return {
                "cpu_frequency_mhz": cpu_freq,
                "cpu_usage_percent": cpu_usage,
                "ram_total_gb": round(ram_info.total / (1024 ** 3), 2),
                "ram_used_gb": round(ram_info.used / (1024 ** 3), 2),
                "ram_available_gb": round(ram_info.available / (1024 ** 3), 2)
            }