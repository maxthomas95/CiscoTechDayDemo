import os
import csv
import meraki
import smtplib
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Fetch env variables
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))  # Ensure this is cast as int
email_user = os.getenv('EMAIL_USER')
email_recipient = os.getenv('EMAIL_RECIPIENT')
key_vault_name = os.getenv('AZURE_KEY_VAULT')

# Set up Azure Key Vault connection
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=kv_uri, credential=credential)
API_KEY = client.get_secret("Meraki-API").value

# Initialize Meraki Dashboard session
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# Define output file path
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'Output')
os.makedirs(output_dir, exist_ok=True)  # Ensures folder exists, but won't create it again if it's already there
CSV_FILE = os.path.join(output_dir, 'meraki_errors.csv')

# Function: Identify clients with 169.x IPs (common misconfig/DHCP issue)
def find_169_client_ips(writer):
    try:
        organizations = dashboard.organizations.getOrganizations()
        print(f"Found {len(organizations)} organizations.")

        for org in organizations:
            networks = dashboard.organizations.getOrganizationNetworks(org['id'])
            print(f"Found {len(networks)} networks in organization {org['id']}.")

            for network in networks:
                network_id = network['id']
                network_name = network['name']

                if network_name.startswith('ATM') or (network_name.startswith('#') and not network_name.startswith('##')):
                    print(f"Skipping network: {network_name} (ID: {network_id})")
                    continue

                clients = dashboard.networks.getNetworkClients(network_id, timespan=86400, perPage=1000, total_pages='all')  # 1 day(s) / Pagination
                print(f"Found {len(clients)} clients in {network_name}")

                for client in clients:
                    ip = client.get('ip') or client.get('recentDeviceIp')
                    if ip and ip.startswith('169'):
                        device_serial = client.get('recentDeviceSerial')
                        if device_serial:
                            device = dashboard.devices.getDevice(device_serial)
                            writer.writerow(['169 Client IP', f"{network_name} - {device['name']}", client.get('description', 'N/A'), client['mac'], ip])
                            print(f"169 IP found: {ip} on {device['name']} in {network_name}")
                        else:
                            print(f"169 IP found: {ip} (no device serial)")
    except Exception as e:
        print(f"[ERROR] 169 check failed: {e}")

# Function: Check MS switch ports for errors or warnings
def check_port_status(network_id, writer):
    try:
        devices = dashboard.networks.getNetworkDevices(network_id)
        for device in devices:
            if 'MS' not in device['model']:
                print(f"Skipping non-MS device: {device['name']}")
                continue

            print(f"Checking MS device: {device['name']}")
            ports = dashboard.switch.getDeviceSwitchPortsStatuses(device['serial'])
            for port in ports:
                if port.get('enabled') and port.get('status') == 'Connected':
                    issues = []
                    if port.get('errors'):
                        issues.extend(port['errors'])
                    if port.get('warnings'):
                        issues.extend(port['warnings'])

                    if issues:
                        issue_list = ', '.join(issues)
                        writer.writerow(['Port Issue', f"{device['name']} - Port {port['portId']}", f"Issues: {issue_list}", port.get('name', 'N/A'), issue_list])
                        print(f"Issues on {device['name']} Port {port['portId']}: {issue_list}")
    except Exception as e:
        print(f"[ERROR] Port check failed: {e}")

# Utility: Get all networks across all orgs
def get_all_networks():
    try:
        all_networks = []
        for org in dashboard.organizations.getOrganizations():
            networks = dashboard.organizations.getOrganizationNetworks(org['id'])
            all_networks.extend(networks)
        return all_networks
    except Exception as e:
        print(f"[ERROR] Failed to fetch networks: {e}")
        return []

# Function: Check all networks (excluding ATM or special ones)
def check_all_networks(writer):
    networks = get_all_networks()
    for network in networks:
        name = network['name']
        if name.startswith('ATM') or name.startswith('#'):
            print(f"Skipping network: {name}")
            continue
        print(f"Checking network: {name}")
        check_port_status(network['id'], writer)

# Email CSV report
def send_email(csv_file):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_recipient
    msg['Subject'] = 'Meraki Errors Report CSV'

    with open(csv_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_file)}')
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(email_user, email_recipient, msg.as_string())
        print(f"Email sent to {email_recipient}")

# Main Execution
def main():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Network/Device Name', 'Description', 'MAC/Port ID', 'IP/Issues'])
        find_169_client_ips(writer)
        check_all_networks(writer)
    send_email(CSV_FILE)

if __name__ == "__main__":
    main()
