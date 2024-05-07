import os
import psutil
import subprocess
import time
import signal
import sys

# Global variables
running = True
last_cpu_usage = 0
last_memory_usage = 0
last_gpu_usage = 0


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_gpu_usage():
    # Use nvidia-smi command to get GPU usage
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"])
        gpu_usage = int(output.decode("utf-8").strip())
        return gpu_usage
    except Exception as e:
        print("Error getting GPU usage:", e)
        return None


def log_stats(cpu_usage, memory_usage, gpu_usage):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(os.path.dirname(__file__), "system_stats.log")
    with open(log_file, "a") as f:
        f.write(f"{timestamp}, CPU: {cpu_usage}%, Memory: {memory_usage}%, GPU: {gpu_usage}%\n")


def signal_handler(sig, frame):
    global running
    global last_cpu_usage, last_memory_usage, last_gpu_usage

    print("Stopping monitoring process...")
    running = False

    # Log the last update
    log_stats(last_cpu_usage, last_memory_usage, last_gpu_usage)
    print("Last update saved to system_stats.log")


if __name__ == "__main__":
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    while running:
        # Update usage values
        last_cpu_usage = get_cpu_usage()
        last_memory_usage = get_memory_usage()
        last_gpu_usage = get_gpu_usage()

        # Sleep for 60 seconds before next update
        time.sleep(60)

    print("Monitoring process stopped.")
    sys.exit(0)
