"""
TuyaPowerGuard - automatic power management based on battery level.

This script monitors the battery level and controls a Tuya smart plug:
- Turns the plug ON when the charge falls below LOW_THRESHOLD
- Turns the plug OFF when the charge exceeds HIGH_THRESHOLD

Configuration is done through environment variables in the .env file
"""
import os
import subprocess
from typing import Optional

from dotenv import load_dotenv
import tinytuya

# Loading environment variables
load_dotenv()

# Configuration
DEVICE_ID = os.getenv("TUYA_POWER_DEVICE_ID")
DEVICE_IP = os.getenv("TUYA_POWER_DEVICE_IP")
DEVICE_KEY = os.getenv("TUYA_POWER_DEVICE_KEY")
LOW_THRESHOLD = int(os.getenv("TUYA_POWER_LOW_THRESHOLD", 40))
HIGH_THRESHOLD = int(os.getenv("TUYA_POWER_HIGH_THRESHOLD", 80))
DEVICE_VERSION = float(os.getenv("TUYA_POWER_DEVICE_VERSION", 3.4))


def get_battery_level() -> int:
    """
    Get the current battery level.
    
    Tries to get data based on the current operating system.
    
    Returns:
        int: Battery level percentage (0-100)
        
    Raises:
        RuntimeError: If unable to get battery level
    """
    import platform
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows method
            result = subprocess.check_output(['powershell', '-Command', 
                                             '(Get-WmiObject win32_battery).EstimatedChargeRemaining'],
                                             stderr=subprocess.STDOUT)
            return int(result.strip())
        elif system == "Linux":
            # Linux method - try several common battery locations
            for path in ['/sys/class/power_supply/BAT0/capacity', 
                         '/sys/class/power_supply/BAT1/capacity',
                         '/sys/class/power_supply/battery/capacity']:
                try:
                    with open(path, 'r') as f:
                        return int(f.read().strip())
                except (FileNotFoundError, IOError):
                    continue
            # If we're here, none of the battery paths worked
            raise FileNotFoundError("No battery information found in expected Linux locations")
        elif system == "Darwin":
            # macOS method using pmset
            result = subprocess.check_output(['pmset', '-g', 'batt'], stderr=subprocess.STDOUT)
            result = result.decode('utf-8')
            percent = int([line for line in result.split('\n') if '%' in line][0].split('\t')[1].split('%')[0])
            return percent
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")
    except (subprocess.SubprocessError, ValueError, IndexError, FileNotFoundError) as e:
        raise RuntimeError(f"Failed to get battery level: {e}")


def control_plug(turn_on: bool) -> None:
    """
    Controls the state of the Tuya smart plug.
    
    Args:
        turn_on (bool): True to turn on, False to turn off
        
    Raises:
        ValueError: If device key is missing
    """
    if not DEVICE_KEY:
        raise ValueError("Error: DEVICE_KEY is missing. Please provide a valid key.")
    
    if not DEVICE_ID or not DEVICE_IP:
        raise ValueError("Error: DEVICE_ID or DEVICE_IP is missing. Check your settings.")
    
    try:
        device = tinytuya.OutletDevice(
            dev_id=DEVICE_ID, 
            address=DEVICE_IP, 
            local_key=DEVICE_KEY, 
            version=DEVICE_VERSION
        )
        
        action = "ON" if turn_on else "OFF"
        print(f"Connecting to device: ID={DEVICE_ID}, IP={DEVICE_IP}")
        
        if turn_on:
            device.turn_on()
        else:
            device.turn_off()
            
        print(f"Plug successfully switched to {action} mode.")
    except Exception as e:
        print(f"Error controlling the plug: {e}")


def main() -> None:
    """
    Main program function.
    
    Checks battery level and controls the plug according to set thresholds.
    """
    try:
        battery_level = get_battery_level()
        print(f"Battery level: {battery_level}%")
        
        if battery_level < LOW_THRESHOLD:
            print(f"Battery level below threshold ({LOW_THRESHOLD}%). Turning plug ON.")
            control_plug(True)
        elif battery_level > HIGH_THRESHOLD:
            print(f"Battery level above threshold ({HIGH_THRESHOLD}%). Turning plug OFF.")
            control_plug(False)
        else:
            print(f"Battery level normal ({LOW_THRESHOLD}%-{HIGH_THRESHOLD}%). Maintaining current state.")
    except Exception as e:
        print(f"Execution error: {e}")


if __name__ == "__main__":
    main()

