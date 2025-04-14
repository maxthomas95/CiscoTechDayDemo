import os
import csv
import meraki
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ============================
# 🔐 Load Environment Variables
# ============================

load_dotenv()

API_KEY = os.getenv("MERAKI_API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

if not API_KEY or not ORGANIZATION_ID:
    raise ValueError("Missing MERAKI_API_KEY or ORGANIZATION_ID. Check your .env file.")

# ============================
# 📦 Set Up Meraki SDK
# ============================

dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# ============================
# 📄 Define CSV Output Path
# ============================

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "Output")
os.makedirs(output_dir, exist_ok=True)

CSV_FILE = os.path.join(output_dir, "meraki_errors.csv")

# ============================
# 🔎 Check for 169.x.x.x Clients
# ============================

def find_169_clients(writer):
    org_networks = dashboard.organizations.getOrganizationNetworks(ORGANIZATION_ID)

    for network in org_networks:
        name = network['name']
        if name.startswith('ATM') or (name.startswith('#') and not name.startswith('##')):
            continue

        clients = dashboard.networks.getNetworkClients(network['id'], timespan=604800, perPage=1000, total_pages='all')

        for client in clients:
            ip = client.get('ip') or client.get('recentDeviceIp')
            if ip and ip.startswith("169"):
                writer.writerow(["169 Client IP", name, client.get('description', 'N/A'), client['mac'], ip])

# ============================
# ⚠️ Check MS Switch Port Errors
# ============================

def check_port_status(writer):
    networks = dashboard.organizations.getOrganizationNetworks(ORGANIZATION_ID)

    for network in networks:
        name = network['name']
        if name.startswith('ATM') or (name.startswith('#') and not name.startswith('##')):
            continue

        devices = dashboard.networks.getNetworkDevices(network['id'])

        for device in devices:
            if "MS" not in device['model']:
                continue

            ports = dashboard.switch.getDeviceSwitchPortsStatuses(device['serial'])

            for port in ports:
                issues = []
                if port.get('errors'):
                    issues.extend(port['errors'])
                if port.get('warnings'):
                    issues.extend(port['warnings'])

                if issues:
                    writer.writerow(["Port Issue", f"{device['name']} - Port {port['portId']}", "Issues Found", port.get('name', 'N/A'), ', '.join(issues)])

# ============================
# 📧 Send CSV Email Report
# ============================

def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = 'Meraki Health Check Report'

    with open(CSV_FILE, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(CSV_FILE)}')
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(EMAIL_USER, EMAIL_RECIPIENT, msg.as_string())

    print(f"✅ Email sent to {EMAIL_RECIPIENT}")

# ============================
# 🚀 Main Execution
# ============================

def main():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Network/Device", "Description", "MAC/Port", "IP/Issues"])
        find_169_clients(writer)
        check_port_status(writer)

    send_email()

if __name__ == "__main__":
    main()
