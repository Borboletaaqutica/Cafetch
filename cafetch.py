import platform
import os
import socket
import psutil
import time
import getpass
import requests
from colorama import Fore, Style, init
import GPUtil

init(autoreset=True)

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    days, remainder = divmod(int(uptime_seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_disk_info():
    partitions = psutil.disk_partitions()
    infos = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            infos.append(f"{p.device} ({p.mountpoint}): {round(usage.used / (1024**3), 2)}GB / {round(usage.total / (1024**3), 2)}GB ({usage.percent}%)")
        except PermissionError:
            continue
    return infos

def get_ip():
    try:
        ip_local = socket.gethostbyname(socket.gethostname())
    except:
        ip_local = "N/A"
    try:
        ip_public = requests.get("https://api.ipify.org").text
    except:
        ip_public = "N/A"
    return ip_local, ip_public

def get_gpu_info():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        return [f"{gpu.name} | {gpu.load*100:.1f}% | {gpu.memoryUsed}/{gpu.memoryTotal}MB" for gpu in gpus]
    except:
        return ["GPU info indisponível (instale GPUtil)"]

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.RED + r"""
       ( (
        ) )
     ........
     |      |]    CAFETCH™
     \      /    
      `----'     
    """ + Style.RESET_ALL)

    user = getpass.getuser()
    local_ip, public_ip = get_ip()

    print(Fore.CYAN + f"{Style.BRIGHT}Usuário:        {Style.NORMAL}{user}")
    print(Fore.CYAN + f"{Style.BRIGHT}Hostname:       {Style.NORMAL}{socket.gethostname()}")
    print(Fore.CYAN + f"{Style.BRIGHT}Sistema:        {Style.NORMAL}{platform.system()} {platform.release()} ({platform.version()})")
    print(Fore.CYAN + f"{Style.BRIGHT}Arquitetura:    {Style.NORMAL}{platform.machine()} | {platform.processor()}")
    print(Fore.CYAN + f"{Style.BRIGHT}Cores (fís/log):{Style.NORMAL}{psutil.cpu_count(logical=False)} / {psutil.cpu_count(logical=True)}")
    print(Fore.CYAN + f"{Style.BRIGHT}Uso CPU:        {Style.NORMAL}{psutil.cpu_percent()}%")
    
    print(Fore.CYAN + f"{Style.BRIGHT}RAM:            {Style.NORMAL}{round(psutil.virtual_memory().used / (1024**3), 2)} / {round(psutil.virtual_memory().total / (1024**3), 2)} GB ({psutil.virtual_memory().percent}%)")
    
    print(Fore.CYAN + f"{Style.BRIGHT}Uptime:         {Style.NORMAL}{get_uptime()}")
    
    print(Fore.CYAN + f"{Style.BRIGHT}IP Local:       {Style.NORMAL}{local_ip}")
    print(Fore.CYAN + f"{Style.BRIGHT}IP Público:     {Style.NORMAL}{public_ip}")

    print(Fore.CYAN + f"{Style.BRIGHT}Discos:")
    for d in get_disk_info():
        print("   " + Fore.YELLOW + d)

    print(Fore.CYAN + f"{Style.BRIGHT}GPU(s):")
    for g in get_gpu_info():
        print("   " + Fore.YELLOW + g)

if __name__ == '__main__':
    main()
