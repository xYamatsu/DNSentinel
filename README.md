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



DNSentinel will automatically configure secure DNS settings and verify the configuration.

Precompiled Executable

If you do not want to install Python, you can download the compiled .exe
version from the Releases section.

The executable performs the same actions as the Python script and only
requires Administrator privileges.

Releases:

https://github.com/YOUR_USERNAME/DNSentinel/releases
Warning

DNSentinel modifies Windows network configuration.

Use this tool only if you understand the changes being applied.

Administrator privileges are required.

Project Structure
DNSentinel/
├ dnsentinel.py
├ README.md
├ LICENSE
└ .gitignore
License

DNSentinel is provided for personal and educational use only.

Commercial use, resale, sublicensing, or redistribution as part of a paid
product is prohibited without written permission from the author.

Contributing

Pull requests and suggestions are welcome.

If you discover a bug or have an improvement idea, please open an issue.

Disclaimer

This software is provided as-is without warranty.

The author is not responsible for any damage or issues caused by the use
of this software.
