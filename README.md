# CiscoTechDayDemo 🔧 Meraki Automation Demo | Presented at Cisco Tech Days Milwaukee, 2025

This script demonstrates how to securely connect to the Meraki Dashboard API using credentials stored in **Azure Key Vault**, retrieve a list of devices in an organization, and export them to a CSV for auditing or inventory purposes.

It's designed to show how easy it is to automate network visibility tasks using Python, Meraki’s REST API, and cloud-based secrets management.

---

## 🚀 What It Does

- Authenticates securely to Azure using a service principal  
- Retrieves a Meraki API key from Azure Key Vault  
- Connects to the Meraki Dashboard API  
- Fetches all devices in a specified organization  
- Writes a CSV with device info: Name, Model, Serial, MAC, Status, IP, Firmware

---

## 🛠 Requirements

- Python 3.8+  
- Azure service principal credentials with access to Key Vault  
- A Meraki API key stored in Azure Key Vault  
- `.env` file with the following environment variables:
```env
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
ORGANIZATION_ID=
```


---

## 📂 File Structure

    CiscoTechDayDemo/
    ├── Python_Scripts/
    │   └── Meraki/
    │       └── Output/
    │           └── devices.csv       # Output CSV file
    ├── main.py                       # Demo script
    └── .env                          # Not committed; holds environment variables



---

## 💡 Why It Matters

Manual inventory and audit tasks slow teams down. With just a few lines of Python, you can automate repetitive tasks, improve visibility, and integrate with secure cloud services like Azure Key Vault.

---

## 🧪 What's Next

This demo is just the beginning — more scripts may be added here in the future to showcase Meraki configuration checks, policy audits, or health reports.


