from fastapi import FastAPI, Query
import re
import subprocess
import psutil

app = FastAPI()

class DeviceSystemInfo:
    def __init__(self):
        pass

    def get_usb_devices(self):
        #regex phân tích output của lệnh lsusb
        device_re = re.compile(r"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb").decode('utf-8')
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)
        return devices
    
    #Lấy thông tin của cpu
    def get_system_info(self):
        cpu_freq = psutil.cpu_freq().current
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        return {
            "cpu_frequency_mhz": cpu_freq,
            "cpu_usage_percent": cpu_usage,
            "ram_total_mb": round(ram_info.total / (1024 ** 3), 2),
            "ram_used_mb": round(ram_info.used / (1024 ** 3), 2),
            "ram_available_mb": round(ram_info.available / (1024 ** 3), 2)
        }
    
    #Kiểm tra ping 
    def get_ping_latency(self, host="google.com"):
        try:
            # Gửi 4 gói tin 
            output = subprocess.check_output(
                ["ping", "-c", "4", host],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            #regex trích xuất giá trị
            latency_re = re.compile(r"rtt min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/\d+\.\d+ ms")
            match = latency_re.search(output)
            
            if match:
                #Độ trễ trung bình
                avg_latency = match.group(1)
                #Độ trễ thấp nhất
                min_latency = match.group(2)
                return {"avg_latency": avg_latency, "min_latency": min_latency}
            else:
                return {"error": "Could not find latency in ping output"}
        
        except subprocess.CalledProcessError as e:
            return {"error": f"Ping command failed: {e}"}
    
system_info_api = DeviceSystemInfo()

@app.get("/api/system-info")
async def system_info():
    return system_info_api.get_system_info()

@app.get("/api/usb-devices")
async def usb_devices():
    return {"devices": system_info_api.get_usb_devices()}

@app.get("/api/ping")
async def ping_latency(host: str = "google.com"):
    return system_info_api.get_ping_latency(host)