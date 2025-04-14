import os
import csv
import meraki
from dotenv import load_dotenv

# ============================
# 🔐 Load Meraki API Key
# ============================

# Load from .env file (recommended for safety)
load_dotenv()
API_KEY = os.getenv("MERAKI_API_KEY")

# OR: Hardcode your API key here (NOT recommended for production)
# API_KEY = "your_api_key_here"

# Your Meraki Organization ID
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

if not API_KEY or not ORGANIZATION_ID:
    raise ValueError("Missing MERAKI_API_KEY or ORGANIZATION_ID. Check your .env file.")

# ============================
# 📦 Set Up Meraki SDK
# ============================

dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# ============================
# 🖥 Get Devices and Save to CSV
# ============================

def main():
    print("Fetching devices from Meraki dashboard...")

    devices = dashboard.organizations.getOrganizationDevices(ORGANIZATION_ID)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "Output")
    os.makedirs(output_dir, exist_ok=True)

    csv_file = os.path.join(output_dir, "devices.csv")

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Model', 'Serial', 'MAC', 'Network ID', 'Status', 'Firmware', 'IP'])

        for device in devices:
            ip = device.get('lanIp', 'N/A')
            writer.writerow([
                device.get('name', ''),
                device.get('model', ''),
                device.get('serial', ''),
                device.get('mac', ''),
                device.get('networkId', ''),
                device.get('status', ''),
                device.get('firmware', ''),
                ip
            ])

    print(f"✅ Device inventory saved to: {csv_file}")

if __name__ == "__main__":
    main()
