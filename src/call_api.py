from fastapi import FastAPI, Query
from api.system_info import SystemInfoAPI
from api.usb_devices import USBDeviceAPI 
from api.ping import PingAPI

app = FastAPI()

@app.get("/api/system-info")
async def system_info():
    return SystemInfoAPI().get_system_info()

@app.get("/api/usb-devices")
async def usb_devices():
    return USBDeviceAPI().get_usb_devices()

@app.get("/api/ping")
async def ping_latency(host: str = "google.com"):
    return PingAPI().get_ping(host)