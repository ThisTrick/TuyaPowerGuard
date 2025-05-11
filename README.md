# TuyaPowerGuard

Automatic power management system based on battery level monitoring. The script continuously checks your device's battery level and controls a Tuya smart plug to:

- Turn the plug **ON** when the battery charge falls below the low threshold (default: 40%)
- Turn the plug **OFF** when the battery charge exceeds the high threshold (default: 80%)

![TuyaPowerGuard](https://img.shields.io/badge/TuyaPowerGuard-v1.0-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Python](https://img.shields.io/badge/Python-3.6+-yellow)

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)
- [License](#license)

## Features

- Cross-platform support (Windows, Linux, macOS)
- Configurable battery thresholds
- Local control of Tuya smart plugs
- Easy configuration via environment variables

## How It Works

TuyaPowerGuard operates on a simple principle:

1. **Monitor**: Periodically checks your device's battery level using system APIs
2. **Analyze**: Compares the current battery level against configured thresholds
3. **Control**: Sends commands to your Tuya smart plug to turn it on/off based on battery status

This creates an automated charging cycle that:
- Prevents overcharging by turning off power when battery is full
- Prevents deep discharge by turning on power when battery gets low
- Extends overall battery life through optimal charge/discharge cycles

```
┌─────────────┐      ┌───────────────┐      ┌────────────┐
│ Get Battery │  →   │ Compare with  │  →   │ Control    │
│ Level       │      │ Thresholds    │      │ Smart Plug │
└─────────────┘      └───────────────┘      └────────────┘
```

## Installation

1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/yourusername/TuyaPowerGuard.git
   cd TuyaPowerGuard
   ```

2. Install required dependencies:
   ```bash
   pip install tinytuya python-dotenv
   ```

3. Create a `.env` file in the project directory:
   ```
   TUYA_POWER_DEVICE_ID=your_device_id
   TUYA_POWER_DEVICE_IP=your_device_ip
   TUYA_POWER_DEVICE_KEY=your_device_local_key
   TUYA_POWER_LOW_THRESHOLD=40
   TUYA_POWER_HIGH_THRESHOLD=80
   TUYA_POWER_DEVICE_VERSION=3.4
   ```

## Configuration

### Finding Your Tuya Device Parameters

To get your device's information:

1. Install TinyTuya:
   ```bash
   pip install tinytuya
   ```

2. Scan for devices on your network:
   ```bash
   python -m tinytuya scan
   ```
   This will list all detected Tuya devices with their IP addresses and Device IDs.

### Obtaining the DEVICE_KEY

To get your device's local key:

1. Use the official Tuya or Smart Life mobile app to set up your device
2. Obtain the key using one of these methods:
   - [TinyTuya Setup Wizard](https://github.com/jasonacox/tinytuya/wiki/Setup-Wizard)
3. Log in to [Tuya IoT Platform](https://iot.tuya.com/)
4. Navigate to Cloud → Development
5. Select your project or create a new one
6. Make sure you've selected the correct data center for your region
7. Enable the necessary API services:
   - IoT Core
   - Authorization
   - Device Control
   - Device Management
8. Link your Smart Life account (Devices → Link App Account → Add)
9. Use the TinyTuya wizard in scan mode:
   ```bash
   python3 -m tinytuya wizard
   ```
10. Update your `.env` file with the obtained key

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| TUYA_POWER_DEVICE_ID | The unique ID of your Tuya device | None |
| TUYA_POWER_DEVICE_IP | IP address of your Tuya device | None |
| TUYA_POWER_DEVICE_KEY | Local key for device access | None |
| TUYA_POWER_LOW_THRESHOLD | Battery percentage to turn plug ON | 40 |
| TUYA_POWER_HIGH_THRESHOLD | Battery percentage to turn plug OFF | 80 |
| TUYA_POWER_DEVICE_VERSION | Protocol version for your device | 3.4 |

## Usage

Run the script manually:

```bash
python TuyaPowerGuard.py
```

### Automated Execution

#### Windows

1. Open Task Scheduler
2. Create a new task:
   - Trigger: Daily, every 5 minutes
   - Action: Start a program, select your Python script
   - Conditions: Run only when connected to network

#### Linux

Add a cron job to run every 5 minutes:

```bash
crontab -e
```

Add this line:
```
*/5 * * * * /usr/bin/python3 /path/to/TuyaPowerGuard.py
```

#### macOS

Use launchd to create a scheduled job:

```bash
# Create a plist file in ~/Library/LaunchAgents/
```

## Troubleshooting

### Common Issues

If you encounter errors when connecting to your Tuya device:

1. **Device not responding**: Make sure the device is powered on and connected to the same network as your computer
2. **Connection timeouts**: Check if the IP address in your .env file is correct and up-to-date
3. **Authentication failures**: Verify that your DEVICE_KEY is correct

### Tuya Cloud Errors

If you see error messages related to Tuya Cloud:

- **"Data center is suspended"** (Code 28841107): Verify your data center configuration in Tuya IoT Platform
- **"Permission deny"** (Code 1106): Check if your Device ID is correct and your account has proper permissions

## Testing

To verify your setup is working correctly:

1. Run the script manually and observe the console output
2. Check if battery level detection works on your system
3. Test if the plug responds to commands when battery is below/above thresholds

## FAQ

### Can I use this with multiple devices?
Yes, you can run multiple instances of TuyaPowerGuard with different configuration files for each device.

### Does this work with all Tuya smart plugs?
TuyaPowerGuard should work with most Tuya-compatible smart plugs that support local control. Some newer devices may require cloud-only access which is not currently supported.

### What if my battery thresholds change seasonally?
You can easily edit the `.env` file to adjust your thresholds without modifying the code.

## System Requirements
- Python 3.6 or newer
- Network connectivity to your Tuya device
- Administrative privileges (for battery level access on some systems)
- Supported operating systems: Windows, macOS, or Linux

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Include your license information here]