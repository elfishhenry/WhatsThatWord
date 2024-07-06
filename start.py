import subprocess
import time

def run_command(command):
    """Runs a command in a separate process."""
    process = subprocess.Popen(command, shell=True)
    return process

if __name__ == "__main__":
    # Commands to run
    commands = [
        "python3 main.py",
        "python3 app.py",
        "ngrok http 5000"
    ]

    # Start each command in a separate process
    processes = [run_command(cmd) for cmd in commands]

    # Keep the script alive to let the processes run
    try:
        while True:
            time.sleep(1)  # Check every second
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Stopping processes...")
        for process in processes:
            process.terminate()
        print("Processes stopped.")
