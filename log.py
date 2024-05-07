import os
import psutil
import subprocess
import time
import signal
import sys

# Global variables
running = True


def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)


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


def get_gpu_memory_usage():
    # Use nvidia-smi command to get GPU memory usage
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"])
        gpu_memory_usage = int(output.decode("utf-8").strip().split()[0])
        return gpu_memory_usage
    except Exception as e:
        print("Error getting GPU memory usage:", e)
        return None


def log_stats(cpu_usage, memory_usage, gpu_usage, gpu_memory_usage):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(os.path.dirname(__file__), "system_stats.log")
    with open(log_file, "a") as f:
        f.write(
            f"{timestamp}, CPU: {cpu_usage}%, Memory: {memory_usage}%, GPU: {gpu_usage}%, GPU Memory: {gpu_memory_usage}MB\n")


def signal_handler(sig, frame):
    global running

    print("Stopping monitoring process...")
    running = False


if __name__ == "__main__":
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    while running:
        # Get system stats
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        gpu_usage = get_gpu_usage()
        gpu_memory_usage = get_gpu_memory_usage()

        # Log the stats
        log_stats(cpu_usage, memory_usage, gpu_usage, gpu_memory_usage)

        # Sleep for 1 second before next update
        time.sleep(1)

    print("Monitoring process stopped.")
    sys.exit(0)
