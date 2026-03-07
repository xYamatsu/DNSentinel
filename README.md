# DNSentinel

DNSentinel is a lightweight Windows privacy hardening tool written in Python.

It automatically configures secure DNS settings, enables encrypted DNS
(DNS over HTTPS), and disables legacy Windows network features that can
expose information on local networks.

DNSentinel helps protect users from DNS leaks, ISP DNS monitoring, and
local network attacks by applying a hardened DNS configuration.

---

## Features

- Configure **Cloudflare DNS** (1.1.1.1 / 1.0.0.1)
- Enable **DNS over HTTPS (DoH)**
- Prevent DNS leaks
- Disable **NetBIOS**
- Disable **LLMNR**
- Disable **mDNS**
- Disable **Smart Multi-Homed Name Resolution**
- Verify DNS encryption and configuration
- Clear error reporting and status output

---

## What DNSentinel Protects Against

DNSentinel improves privacy against:

- ISP DNS tracking
- DNS spoofing
- Malicious public Wi-Fi networks
- Local network credential interception attacks
- DNS broadcast leaks

---

## Requirements

- Windows 10 / Windows 11
- Administrator privileges

If running from source:

- Python **3.9+**

---

## Usage

### Run from Python

Run the script as **Administrator**:

```bash
python dnsentinel.py
