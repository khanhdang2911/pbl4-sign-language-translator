from typing import Dict
import subprocess
import re

class PingAPI:
    #Kiểm tra ping 
    def get_ping(self, host="google.com"):
        try:
            # Gửi 4 gói tin 
            output = subprocess.check_output(
                ["ping", "-c", "4", host],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            #regex trích xuất giá trị
            latency_regex = re.compile(r"rtt min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/\d+\.\d+ ms")
            match = latency_regex.search(output)
            
            if match:
                #Độ trễ trung bình
                avg_latency = match.group(2)
                #Độ trễ thấp nhất
                min_latency = match.group(1)
                return {"Ping to":host,"avg_latency": avg_latency, "min_latency": min_latency}
            else:
                return {"error": "Could not find latency in ping output"}
        
        except subprocess.CalledProcessError as e:
            return {"error": f"Ping command failed: {e}"}