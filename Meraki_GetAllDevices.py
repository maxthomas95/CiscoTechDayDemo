import os
import csv
import meraki
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Grab secrets for Azure + Meraki integration
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
organization_id = os.getenv('ORGANIZATION_ID')

# Connect to Azure Key Vault to get the Meraki API key
key_vault_name = "infra-keyvault-prod-kv"
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)
API_KEY = client.get_secret("Meraki-API").value

# Initialize Meraki Dashboard API session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Fetch all devices from the organization
devices = dashboard.organizations.getOrganizationDevices(organization_id)

# Define output file path
folder_path = 'Python_Scripts/Meraki/Output'
csv_file_name = os.path.join(folder_path, 'devices.csv')

# Write device details to CSV
def write_to_csv(devices, filename=csv_file_name):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Model', 'Serial', 'MAC', 'Network ID', 'Status', 'Firmware', 'IP'])
        for device in devices:
            ip = device.get('lanIp', 'N/A')  # Some devices may not have a LAN IP
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
            
# Execute the export
write_to_csv(devices)
print(f"CSV file created at: {csv_file_name}")
print("All device information has been successfully written to devices.csv")