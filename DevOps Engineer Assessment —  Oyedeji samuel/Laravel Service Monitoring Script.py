import psutil
import os

if psutil.cpu_percent() > 80:
    os.system("systemctl restart laravel-backend")
