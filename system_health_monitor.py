import psutil
import logging
import time
from logging.handlers import RotatingFileHandler

# Configure rotating log handler (recommended for long-running monitors)
handler = RotatingFileHandler('system_health.log', maxBytes=5_000_000, backupCount=3)
logging.basicConfig(level=logging.INFO, handlers=[handler], format='%(asctime)s - %(levelname)s - %(message)s')

# Thresholds
CPU_THRESHOLD = 80.0  # in percentage
MEMORY_THRESHOLD = 80.0  # in percentage
DISK_THRESHOLD = 80.0  # in percentage
PROCESS_COUNT_THRESHOLD = 300  # arbitrary process count threshold

def check_cpu_usage():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
    except Exception as e:
        logging.error(f'CPU check failed: {e}')
        return None
    if cpu_usage is not None and cpu_usage > CPU_THRESHOLD:
        logging.warning(f'High CPU usage detected: {cpu_usage}%')
    return cpu_usage

def check_memory_usage():
    try:
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
    except Exception as e:
        logging.error(f'Memory check failed: {e}')
        return None
    if memory_usage is not None and memory_usage > MEMORY_THRESHOLD:
        logging.warning(f'High Memory usage detected: {memory_usage}%')
    return memory_usage

def check_disk_space(path='/'):
    try:
        disk = psutil.disk_usage(path)
        disk_usage = disk.percent
    except Exception as e:
        logging.error(f'Disk check failed: {e}')
        return None
    if disk_usage is not None and disk_usage > DISK_THRESHOLD:
        logging.warning(f'Low Disk space detected: {disk_usage}% used')
    return disk_usage

def check_running_processes():
    try:
        process_count = len(psutil.pids())
    except Exception as e:
        logging.error(f'Process check failed: {e}')
        return None
    if process_count is not None and process_count > PROCESS_COUNT_THRESHOLD:
        logging.warning(f'High number of processes running: {process_count}')
    return process_count

def log_system_health():
    cpu = check_cpu_usage()
    memory = check_memory_usage()
    disk = check_disk_space()
    processes = check_running_processes()

    logging.info(f'System Health - CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%, Processes: {processes}')

def monitor_forever(interval=60):
    while True:
        log_system_health()
        time.sleep(interval)

if __name__ == '__main__':
    # default single-run; change to monitor_forever() to run continuously
    log_system_health()
