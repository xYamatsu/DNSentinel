import subprocess
import ctypes
import sys

# -----------------------------
# Admin check
# -----------------------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# -----------------------------
# Command runner with output
# -----------------------------

def run(cmd, description):

    print(f"\n[+] {description}")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[OK] Command executed successfully")
        else:
            print("[ERROR]")
            print(result.stderr)

    except Exception as e:
        print("[EXCEPTION]", e)


# -----------------------------
# DNS configuration
# -----------------------------

def set_cloudflare_dns():

    run(
        'netsh interface ipv4 set dnsservers name="Ethernet" source=static address=1.1.1.1 register=none',
        "Setting Cloudflare primary DNS"
    )

    run(
        'netsh interface ipv4 add dnsservers name="Ethernet" address=1.0.0.1 index=2',
        "Setting Cloudflare secondary DNS"
    )


# -----------------------------
# Enable DNS over HTTPS
# -----------------------------

def enable_doh():

    run(
        'netsh dns add encryption server=1.1.1.1 dohtemplate=https://cloudflare-dns.com/dns-query autoupgrade=yes',
        "Enabling DoH for 1.1.1.1"
    )

    run(
        'netsh dns add encryption server=1.0.0.1 dohtemplate=https://cloudflare-dns.com/dns-query autoupgrade=yes',
        "Enabling DoH for 1.0.0.1"
    )

    run(
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters" /v EnableAutoDoh /t REG_DWORD /d 2 /f',
        "Enabling automatic DoH upgrade"
    )


# -----------------------------
# Disable NetBIOS
# -----------------------------

def disable_netbios():

    run(
        'powershell -Command "Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $true} | ForEach-Object {$_.SetTcpipNetbios(2)}"',
        "Disabling NetBIOS"
    )


# -----------------------------
# Disable LLMNR
# -----------------------------

def disable_llmnr():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f',
        "Disabling LLMNR"
    )


# -----------------------------
# Disable mDNS
# -----------------------------

def disable_mdns():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v EnableMDNS /t REG_DWORD /d 0 /f',
        "Disabling mDNS"
    )


# -----------------------------
# Disable Smart DNS fallback
# -----------------------------

def disable_smart_dns():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v DisableSmartNameResolution /t REG_DWORD /d 1 /f',
        "Disabling Smart Multi-Homed Name Resolution"
    )


# -----------------------------
# Verify configuration
# -----------------------------

def verify():

    run("ipconfig /all", "Displaying network configuration")
    run("netsh dns show encryption", "Showing DNS encryption status")


# -----------------------------
# Main
# -----------------------------

def main():

    print("\n=== DNSentinel Privacy Hardening Tool ===\n")

    if not is_admin():
        print("Please run this program as Administrator.")
        sys.exit()

    set_cloudflare_dns()
    enable_doh()

    disable_netbios()
    disable_llmnr()
    disable_mdns()
    disable_smart_dns()

    verify()

    print("\n[✓] DNSentinel configuration complete.\n")


if __name__ == "__main__":
    main()