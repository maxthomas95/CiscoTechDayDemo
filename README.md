# CiscoTechDayDemo 🔧 Meraki Automation Demo | Presented at Cisco Tech Days Milwaukee, 2025

This repo demonstrates real-world Meraki automation techniques using Python and Azure Key Vault. It includes two example scripts designed to improve visibility, reduce manual work, and showcase what’s possible with just a bit of code.

---

## 🚀 What It Does

### ✅ Audit Script: `Meraki_GetAllDevices.py`
- Authenticates securely to Azure using a service principal  
- Retrieves a Meraki API key from Azure Key Vault  
- Connects to the Meraki Dashboard API  
- Fetches all devices in a specified organization  
- Exports a CSV with device info: Name, Model, Serial, MAC, Status, IP, Firmware  

### 🔍 Health Check Script: `Meraki_Check_AllErrors.py`
- Scans Meraki clients for `169.x.x.x` IP addresses (common DHCP issue)  
- Analyzes MS switch ports for any warnings or error flags  
- Skips certain networks by naming convention (`ATM-`, `#`, etc.)  
- Writes a unified CSV report of client anomalies and port issues  
- Emails the report automatically to a designated recipient  

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
KEY_VAULT_NAME=
SMTP_SERVER=
SMTP_PORT=
EMAIL_USER=
EMAIL_RECIPIENT=
```

---

## 📂 File Structure

```text
CiscoTechDayDemo/
├── Python_Scripts/
│   └── Meraki/
│       ├── Meraki_Audit_DeviceInventory.py
│       ├── Meraki_Check_AllErrors.py
│       └── Output/
│           ├── devices.csv
│           └── meraki_errors.csv
├── .env  (not committed)
└── README.md
```

---

## 💡 Why It Matters

Manual inventory checks and config audits eat up time — especially during audits or incident response. These scripts show how automation with Meraki’s API can:
- Save time and reduce human error  
- Provide continuous visibility into your network health  
- Integrate securely with cloud-native tools like Azure Key Vault  

---

## 🧪 What's Next

This demo is just the beginning — more scripts may be added here in the future to showcase Meraki configuration checks, policy audits, or health reports.

---

Built with 💻 and ☕ by [Max Thomas](https://github.com/maxthomas95)

