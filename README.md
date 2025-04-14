# CiscoTechDayDemo 🔧 Meraki Automation Demo | Presented at Cisco Tech Days Milwaukee, 2025

This repo showcases how you can automate real-world Meraki workflows using Python and the Meraki Dashboard API — from basic inventory pulls to proactive network health checks.

---

## 🚀 What’s Inside

This project includes two core scripts — each available in:

- A **basic version** for beginners or quick testing (no Azure setup needed)
- A **secure version** using Azure Key Vault for real-world deployments

---

### ✅ Audit Script

**Purpose:** Pull a full device inventory from your Meraki organization and save it to CSV.

- **🔹 Basic:** [`Meraki_Audit_DeviceInventory_basic.py`](./Python_Scripts/Meraki/Basic/Meraki_Audit_DeviceInventory_basic.py)  
  Quickly pulls a full device inventory from your Meraki organization and saves it to a CSV.  
  Uses `.env` for API key and Org ID — no external dependencies.  
  *Perfect for audits, asset tracking, DevNet learners.*

- **🔐 Secure:** [`Meraki_Audit_DeviceInventory.py`](./Python_Scripts/Meraki/Secure/Meraki_Audit_DeviceInventory.py)  
  Same inventory logic — but securely pulls secrets from Azure Key Vault and uses a service principal to authenticate.

---

### 🔍 Health Check Script

**Purpose:** Identify issues like 169.x.x.x IPs and Meraki switch port errors.

- **🔹 Basic:** [`Meraki_Check_AllErrors_basic.py`](./Python_Scripts/Meraki/Basic/Meraki_Check_AllErrors_basic.py)  
  Scans Meraki clients for `169.x.x.x` IPs and MS switch ports for error/warning flags.  
  Sends the results via email as a CSV attachment.  
  *Great for weekly network health checks, monitoring, and proactive support.*

- **🔐 Secure:** [`Meraki_Check_AllErrors.py`](./Python_Scripts/Meraki/Secure/Meraki_Check_AllErrors.py)  
  Production-ready version with cloud-based secrets, environment filtering, and improved handling for enterprise use.

---

## 🛠 Requirements

### For Secure Versions (Azure Key Vault)

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

### For Basic Versions (Quick Start)

Just want to test things quickly without setting up Azure Key Vault?

- Python 3.8+
- `.env` file with:
```env
MERAKI_API_KEY=your_api_key_here
ORGANIZATION_ID=your_org_id_here
```

Only needed for the health check script — add these too:

```env
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587
EMAIL_USER=you@yourdomain.com
EMAIL_RECIPIENT=someone@yourdomain.com
```
---

## 🔐 For Production Use

If you’re ready to build something secure and scalable, check out the versions under `Secure/` which use:
- Azure Key Vault for secrets
- Service principal auth
- Better exception handling and modular code

---

## 📂 File Structure

```text
CiscoTechDayDemo/
├── Python_Scripts/
│   └── Meraki/
│       ├── Secure/
│       │   ├── Meraki_Audit_DeviceInventory.py
│       │   ├── Meraki_Check_AllErrors.py
│       ├── Basic/
│       │   ├── Meraki_Audit_DeviceInventory_basic.py
│       │   ├── Meraki_Check_AllErrors_basic.py
│       └── Output/
│           ├── devices.csv
│           └── meraki_errors.csv
├── .env.example
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

